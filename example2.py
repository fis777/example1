import unittest


def is_even(number):
    ''' Returns True if **number** is even or False if it is odd. '''
    return number % 2


class TestEvenOdd(unittest.TestCase):

    def test_even(self):
        self.assertTrue(is_even(2))

    def test_odd(self):
        self.assertFalse(is_even(3))

    def test_zero(self):
        with self.assertRaises(ValueError):
            is_even(0)


if __name__ == '__main__':
    unittest.main()
