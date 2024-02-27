from unittest import TestCase

from main import *


class ConfigTest(TestCase):
    def test_load_config_not_null(self):
        config = load_config()
        assert config is not None

    def test_gears_load(self):
        config = load_config()
        assert len(config["gears"]) > 0


class GetCarFromListTest(TestCase):

    def test_get_car_from_list(self):
        cars_list = [Car(current_gear=0,
                         car_type="abc",
                         vin="abc123",
                         current_speed=0)]
        car = get_car_from_list(0, cars_list)
        assert car is not None

    def test_get_car_from_list_invalid_index(self):
        cars_list = [Car(current_gear=0,
                         car_type="abc",
                         vin="abc123",
                         current_speed=0)]
        car = get_car_from_list(-1, cars_list)
        assert car is None

    def test_get_car_from_list_invalid_index1(self):
        cars_list = [Car(current_gear=0,
                         car_type="abc",
                         vin="abc123",
                         current_speed=0)]

        car = get_car_from_list(15, cars_list)
        assert car is None


class GetCarGearsTest(TestCase):

    def test_get_car_gears_null_check(self):
        config = load_config()
        l = get_car_gears(config)
        assert l is not None

    def test_get_car_gears_empty(self):
        config = load_config()
        l = get_car_gears(config)
        assert len(l) > 0

    def test_get_car_gears_six_elements(self):
        config = load_config()
        l = get_car_gears(config)
        assert len(l) == 6


class ChangeGears(TestCase):

    def test_change_gears1(self):
        config = load_config()
        gears = get_car_gears(config)
        car = Car(current_gear=0,
                  car_type="abc",
                  vin="abc123",
                  current_speed=0)

        change_gears(car, gears[1], gears)

        assert car.current_gear == gears[1][0]

    def test_change_gears2(self):
        config = load_config()
        gears = get_car_gears(config)
        car = Car(current_gear=0,
                  car_type="abc",
                  vin="abc123",
                  current_speed=0)

        change_gears(car, gears[2], gears)

        assert car.current_gear == gears[2][0]

    def test_change_gears3(self):
        config = load_config()
        gears = get_car_gears(config)
        car = Car(current_gear=1,
                  car_type="abc",
                  vin="abc123",
                  current_speed=0)

        change_gears(car, gears[2], gears)

        assert car.current_gear == gears[2][0]

    def test_change_gears4(self):
        config = load_config()
        gears = get_car_gears(config)
        car = Car(current_gear=3,
                  car_type="abc",
                  vin="abc123",
                  current_speed=0)

        change_gears(car, gears[4], gears)

        assert car.current_gear == gears[4][0]