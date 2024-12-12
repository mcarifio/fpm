import unittest


class TestCase(unittest.TestCase):
    def test_always_passes(self):
        self.assertTrue(True)


def on_test():
    unittest.main(verbosity=2)


if __name__ == "__main__":
    on_test()
