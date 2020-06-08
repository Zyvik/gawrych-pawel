import unittest
import chapter3


class TestChapter3(unittest.TestCase):

    def test_is_rising_valid(self):
        valid_nums = [1111, 1222, 1234]
        for n in valid_nums:
            password = chapter3.Password(n)
            self.assertTrue(password.is_rising())

    def test_is_rising_invalid(self):
        invalid_nums = [1231, 54678, 12340234]
        for n in invalid_nums:
            password = chapter3.Password(n)
            self.assertFalse(password.is_rising())

    def test_has_two_clusters_valid(self):
        valid_nums = [111122, 1122, 444455, 111000, 11223334440006666]
        for n in valid_nums:
            password = chapter3.Password(n)
            self.assertTrue(password.has_two_clusters())

    def test_has_two_clusters_invalid(self):
        invalid_nums = [1111, 12345, 121212122, 44567]
        for n in invalid_nums:
            password = chapter3.Password(n)
            self.assertFalse(password.has_two_clusters())

    def test_set_next_rising_number(self):

        decreasing_password = chapter3.Password(56123049)
        decreasing_password.set_next_rising_number(2, 6)
        self.assertEqual(decreasing_password.next_rising_number, 56666666)


if __name__ == '__main__':
    unittest.main()
