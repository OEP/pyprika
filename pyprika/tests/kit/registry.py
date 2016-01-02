import pkg_resources
import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest
from pyprika.kit.registry import _Registry as Registry

FIXTURE_ROOT = pkg_resources.resource_filename('pyprika',
                                               'tests/kit/fixtures')
FIXTURE_SIMPLE = pkg_resources.resource_filename('pyprika',
                                                 'tests/kit/fixtures/simple')


class RegistryTestCase(unittest.TestCase):

    def setUp(self):
        self.registry = Registry()

    def test_search(self):
        self.registry.search(FIXTURE_SIMPLE)
        result = self.registry.recipes.keys()
        expected = ['w01']
        self.assertItemsEqual(expected, result)

    def test_search_shallow(self):
        self.registry.search(FIXTURE_ROOT)
        result = self.registry.recipes.keys()
        expected = ['no-index-recipe']
        self.assertItemsEqual(expected, result)

    def test_recursive_search(self):
        self.registry.recursive_search(FIXTURE_ROOT)
        result = self.registry.recipes.keys()
        expected = ['no-index-recipe', 'w01']
        self.assertItemsEqual(expected, result)
