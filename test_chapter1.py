import unittest
from chapter1 import Car, IllegalCarError


class TestCar(unittest.TestCase):

    def test_init_invalid_type(self):
        self.assertRaises(TypeError, Car, 'foobar', 1, 1)
        self.assertRaises(TypeError, Car, 1, 'foobar', 1)
        self.assertRaises(TypeError, Car, 1, 1, 'foobar')

    def test_init_invalid_pax_count(self):
        self.assertRaises(IllegalCarError, Car, 0, 1, 1)
        self.assertRaises(IllegalCarError, Car, 6, 1, 1)

    def test_init_invalid_car_mass(self):
        self.assertRaises(IllegalCarError, Car, 1, 0, 1)
        self.assertRaises(IllegalCarError, Car, 1, 2001, 1)

    def test_init_invalid_gear_count(self):
        self.assertRaises(IllegalCarError, Car, 1, 1, 0)

    def test_init_valid(self):
        edge_case_car_1 = Car(1, 0.0001, 1)  # almost edge cases ;)
        edge_case_car_2 = Car(5, 2000, 10000)
        self.assertTrue(edge_case_car_1)
        self.assertTrue(edge_case_car_2)

    def test_total_mass(self):
        car = Car(1, 1, 1)
        expected_mass = car.pax_count * car.PAX_MASS + car.car_mass
        self.assertEqual(car.total_mass, expected_mass)

    def test_total_mass_value_change_valid(self):
        car = Car(1, 1, 1)
        initial_total_mass = car.total_mass
        car.pax_count += 1
        expected_total_mass = initial_total_mass + car.PAX_MASS
        self.assertEqual(car.total_mass, expected_total_mass)

    # Tests under this are propably redundant. I'm keeping them just in case.
    def test_total_mass_value_change_invalid(self):
        car = Car(1, 1, 1)
        initial_total_mass = car.total_mass
        try:
            car.pax_count = 0
            self.fail()
        except IllegalCarError:
            self.assertEqual(car.total_mass, initial_total_mass)

    def test_argument_change_invalid(self):
        car = Car(1, 1, 1)
        try:
            car.car_mass = 2001
            self.fail()
        except IllegalCarError:
            self.assertEqual(car.car_mass, 1)

        try:
            car.pax_count = 6
            self.fail()
        except IllegalCarError:
            self.assertEqual(car.pax_count, 1)

        try:
            car.gear_count = -1
            self.fail()
        except IllegalCarError:
            self.assertEqual(car.gear_count, 1)


if __name__ == '__main__':
    unittest.main()
