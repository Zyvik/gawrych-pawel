class IllegalCarError(Exception):
    pass


class Car:
    MAX_PAX_COUNT = 5
    MAX_CAR_MASS = 2000  # in kg
    PAX_MASS = 70  # average passeneger mass in kg

    def __init__(self, pax_count, car_mass, gear_count):
        self.pax_count = pax_count
        self.car_mass = car_mass
        self.gear_count = gear_count

    def __repr__(self):
        return f"Car({self.pax_count}, {self.car_mass}, {self.gear_count})"

    def __str__(self):
        string = f"Car - passenegers: {self.pax_count}," \
                 f" mass: {self.car_mass}kg, gears: {self.gear_count}"
        return string

    @property
    def pax_count(self):
        return self._pax_count

    @pax_count.setter
    def pax_count(self, pax_count):
        if not isinstance(pax_count, int):
            raise TypeError('pax_count has to be an integer.')
        if not 1 <= pax_count <= self.MAX_PAX_COUNT:
            error_msg = "Illegal numer of passengers. (1-5 allowed)"
            raise IllegalCarError(error_msg)
        self._pax_count = pax_count

    @property
    def car_mass(self):
        return self._car_mass

    @car_mass.setter
    def car_mass(self, car_mass):
        if not (isinstance(car_mass, int) or isinstance(car_mass, float)):
            error_msg = 'car_mass has to be an integer or a folat'
            raise TypeError(error_msg)
        if not 0 < car_mass <= self.MAX_CAR_MASS:
            error_msg = f"Car is too heavy (over {self.MAX_CAR_MASS}kg)" \
                        "or breaks laws of physics."
            raise IllegalCarError(error_msg)
        self._car_mass = car_mass

    @property
    def gear_count(self):
        return self._gear_count

    @gear_count.setter
    def gear_count(self, gear_count):
        # It wasn't specified in the task but I did't want to bother Dagmara,
        # so I've figured that a car has to have at least 1 gear...
        if not isinstance(gear_count, int):
            error_msg = 'gear_count has to be positive integer'
            raise TypeError(error_msg)
        if gear_count < 1:
            error_msg = "A car has to have at least 1 gear."
            raise IllegalCarError(error_msg)
        self._gear_count = gear_count

    @property
    def total_mass(self):
        return self.car_mass + self.pax_count * self.PAX_MASS
