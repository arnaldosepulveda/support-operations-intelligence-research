import unittest

import support_operations_intelligence


class PackageBoundaryTests(unittest.TestCase):
    def test_package_imports(self):
        self.assertIsNotNone(support_operations_intelligence)


if __name__ == "__main__":
    unittest.main()
