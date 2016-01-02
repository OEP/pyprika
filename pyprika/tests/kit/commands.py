import os
import sys
import pkg_resources
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from pyprika.kit import commands
from pyprika.kit.commands import CommandError
from pyprika.kit.registry import _Registry as Registry

FIXTURE_ROOT = pkg_resources.resource_filename('pyprika',
                                               'tests/kit/fixtures')
FIXTURE_SIMPLE = pkg_resources.resource_filename('pyprika',
                                                 'tests/kit/fixtures/simple')


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.stdout = StringIO()
        self.stderr = StringIO()
        self.command = self._get_command()
        self.command.stdout = self.stdout
        self.command.stderr = self.stderr
        self.command.registry = Registry(paths=FIXTURE_SIMPLE)

    def run_command(self, *args):
        self.command.run(*args)
        self.stdout.seek(0)
        self.stderr.seek(0)

    def _nostdout(self):
        self.stderr.seek(0)
        self.assertEqual('', self.stderr.getvalue())

    def _nostderr(self):
        self.stderr.seek(0)
        self.assertEqual('', self.stderr.getvalue())


class ListTestCase(BaseTestCase):
    def _get_command(self):
        return commands.List()

    def test_run1(self):
        self.run_command()
        expected = 'w01 Water\n'
        result = self.stdout.getvalue()
        self.assertEqual(expected, result)
        self._nostderr()


class SearchTestCase(BaseTestCase):
    def _get_command(self):
        return commands.Search()

    def test_run1(self):
        self.run_command('water')
        self._nostdout()
        self._nostderr()

    def test_run2(self):
        self.run_command('-i', 'water')
        expected = 'w01 Water\n'
        result = self.stdout.getvalue()
        self.assertEqual(expected, result)
        self._nostderr()


class ShowTestCase(BaseTestCase):
    def _get_command(self):
        return commands.Show()

    def test_run1(self):
        self.run_command('w01')
        expected = '''\
Name: Water

Ingredients:

  - water

Directions:

  1. drink
'''
        result = self.stdout.getvalue()
        self.assertEqual(expected, result)
        self._nostderr()

    @unittest.skipIf(sys.version_info < (2, 7),
                     'no assertRaises() context manager support')
    def test_run2(self):
        with self.assertRaises(CommandError) as cm:
            self.run_command('w01', '-s', 'booga')
        result = cm.exception.message
        expected = 'not a valid number: booga'
        self.assertEqual(expected, result)


class ValidateTestCase(BaseTestCase):
    error = os.path.join(FIXTURE_ROOT, 'error.yaml')
    ok = os.path.join(FIXTURE_SIMPLE, 'water.yaml')

    def _get_command(self):
        return commands.Validate()

    def test_run1(self):
        self.run_command(self.error)
        expected = "Not a valid number: '1.1.1'\n"
        result = self.stdout.getvalue()
        self.assertEqual(expected, result)
        self._nostderr()

    def test_run2(self):
        self.run_command(self.ok, self.error)
        expected = "%s: Not a valid number: '1.1.1'\n" % self.error
        result = self.stdout.getvalue()
        self.assertEqual(expected, result)
        self._nostderr()


class WhichTestCase(BaseTestCase):
    def _get_command(self):
        return commands.Which()

    def test_run1(self):
        self.run_command('w01')
        expected = os.path.join(FIXTURE_SIMPLE, 'water.yaml') + '\n'
        result = self.stdout.getvalue()
        self.assertEqual(expected, result)

    @unittest.skipIf(sys.version_info < (2, 7),
                     'no assertRaises() context manager support')
    def test_run2(self):
        with self.assertRaises(CommandError) as cm:
            self.run_command('xxx')
        result = cm.exception.message
        expected = 'no matches for `xxx`'
        self.assertEqual(expected, result)


class PrivateTestCase(unittest.TestCase):
    def test_suggest_2arg(self):
        result = commands._suggest(('a', 'b'))
        expected = 'a or b'
        self.assertEqual(expected, result)

    def test_suggest_3arg(self):
        result = commands._suggest(('a', 'b', 'c'))
        expected = 'a, b or c'
        self.assertEqual(expected, result)

    def test_suggest_4arg(self):
        result = commands._suggest(('a', 'b', 'c', 'd'))
        expected = 'a, b, c...'
        self.assertEqual(expected, result)

    def test_suggest_prefix(self):
        result = commands._suggest(('pretty', 'prance', 'prince'))
        expected = 'pre, pra or pri'
        self.assertEqual(expected, result)
