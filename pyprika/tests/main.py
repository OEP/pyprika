from unittest import TestSuite, findTestCases, TextTestRunner
from . import recipe, ingredient, quantity

TEST_MODULES = (
  recipe,
  ingredient,
  quantity,
)

if __name__ == "__main__":
  runner = TextTestRunner()
  suites = [findTestCases(m) for m in TEST_MODULES]
  suite = TestSuite(suites)
  runner.run(suite)
