#!/usr/bin/env python
"""
This program simulates shift changes in a car.
"""
import csv
import pytz
import logging as logger
import configparser
import random

from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple

logger.basicConfig(
    level=logger.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logger.FileHandler("debug.log", "a")
    ]
)


class ProcessingException(Exception):
    """ General Exception """
    pass


@dataclass
class Car:
    """
    This class object represents a car.
    """
    current_speed: int
    current_gear: int
    vin: str
    car_type: str


def load_config() -> configparser.ConfigParser:
    """
    This function loads the config file.
    :returns: configparser.ConfigParser
    """
    config_parser = configparser.ConfigParser()
    config_parser.read("./config.ini")
    return config_parser


def print_menu() -> None:
    """
    Prints menu to screen.
    :return: None
    """
    print("1. Create Car.")
    print("2. Print car details")
    print("3. Select car and change gears.")
    print("Q. Quit.\n")


def print_car_detail(car: Car,
                     index: int = -2) -> None:
    """
    Prints car detail.
    :param car:
    :param index:
    :return:
    """
    if car and index:
        print("------")
        msg = f"Car vin: {car.vin} type: {car.car_type} speed: {car.current_speed} gear: {car.current_gear}"
        if index > -1:
            msg = f"{index}: {msg}"
        print(msg)
        print("------\n")


def print_car_list(car_list: List[Car]) -> None:
    """
    Prints car details in list.
    """
    if car_list:
        for i, car in enumerate(car_list):
            print_car_detail(car, i)


def print_gears_list(gears: List[Tuple[int, int, int]]) -> None:
    """
    Prints the gears in a car.
    :param gears:
    :return: None
    """
    if gears:
        for (index, low_speed, high_speed) in gears:
            print(f"{index}: {low_speed} - {high_speed}\n")


def get_user_input(prompt: str) -> str:
    """
    Get User Input from keyboard.
    :param prompt: str
    :return:
    """
    value = input(f"{prompt}\n")
    return value.strip()


def get_car_from_list(index: int,
                      car_list: List[Car]) -> Car:
    """
    Gets a car from a list of cars.
    :param index:
    :param car_list:
    :return:
    """
    if index > -1 and (index <= len(car_list)):
        return car_list[index]


def get_car_gears(configs: configparser.ConfigParser) -> List[Tuple[int, int, int]]:
    """
    Loads
    :param configs:
    :return:
    """
    gear_list = []
    if configs:
        index = 1
        tmp = f"gear_{index}"
        while tmp in configs["gears"]:
            setting = configs["gears"][tmp]

            values = [x.strip() for x in setting.split(',')]
            gear_list.append((index - 1,
                              int(values[0]),
                              int(values[1], )))
            index += 1
            tmp = f"gear_{index}"
    return gear_list


def get_utc_epoch():
    """
    Get epoch time since 1970
    :return:
    """
    current_time_utc = datetime.now(pytz.utc)
    epoch_difference = current_time_utc - datetime(1970, 1, 1, tzinfo=pytz.utc)
    epoch_time = epoch_difference.total_seconds()
    return epoch_time


def write_event(car: Car,
                speed: int,
                gear: int) -> None:
    """
    Writes gear changes to csv file
    :param car:
    :param speed:
    :param gear:
    :return: None
    """
    logger.info(f"Switching Gears - vin: {car.vin} - gear: {gear}")
    with open("events.csv", "a") as file:
        writer = csv.writer(file)

        writer.writerow([int(get_utc_epoch()),
                         car.vin,
                         car.car_type,
                         car.current_speed,
                         car.current_gear,
                         speed,
                         gear])
        file.flush()


def create_car(car_type: str, vin: str) -> Car:
    """
    Creates new car
    :param car_type:
    :param vin:
    :return:
    """
    car: Car = Car(vin=vin,
                   car_type=car_type,
                   current_speed=0,
                   current_gear=0)
    msg: str = f"Created new Car: {car.vin} - {car.car_type}"
    logger.info(msg)
    print_car_detail(car)
    return car


def change_gears(car: Car,
                 future_gear: Tuple[int, int, int],
                 gears_list: List[Tuple[int, int, int]]):
    logger.debug(f"Car: {car.vin} gear: {gears_list[car.current_gear]}")
    logger.debug(f"Changing Gears: {car.vin} - {future_gear}")
    logger.info("Car: %s switching to gear: %d", car.vin, future_gear[0])

    flag = True
    while flag:
        # Accelerate
        if car.current_gear < future_gear[0]:
            for i, gear in enumerate(gears_list):
                # break out of loop.
                if car.current_gear == future_gear[0]:
                    flag = False
                    break
                elif car.current_gear >= i:
                    speed_change = random.randint(1, 6)
                    write_event(car, speed_change, i)
                    car.current_speed = random.randint(gear[1], gear[2])
                    car.current_gear = i + 1
                    logger.debug(f"\t{car}")


def run(config_func):
    """
    This function runs
    :param config_func:
    :return:
    """
    config: configparser.ConfigParser = config_func()
    gears_list: List[Tuple[int, int, int]] = get_car_gears(config)
    car_list: List[Car] = [create_car("toyota", "1234yes")]

    while True:
        try:
            print_menu()
            value = get_user_input("Please make selection: ")

            if value == "1":
                car_type = get_user_input("Please enter type: ")
                vin = get_user_input("Please enter vin: ")
                car_list.append(create_car(car_type, vin))

            if value == "2" and len(car_list) > 0:
                logger.debug("printing menu.")
                print_car_list(car_list)

            if value == "3" and len(car_list) > 0:
                print_car_list(car_list)
                value = int(get_user_input("Please choose car: "))

                car = get_car_from_list(value, car_list)
                logger.info("Car chosen: %s", car.vin)

                if car is None:
                    raise Exception(f"Invalid selection: {value}")

                print_gears_list(gears_list)

                gear_value = int(get_user_input("Please select gear: "))

                list_of_gears = [x[0] for x in gears_list]

                if gear_value not in list_of_gears:
                    raise Exception(f"Invalid selection: {value}")

                gear = gears_list[gear_value]

                if gear[0] == car.current_gear:
                    raise Exception(f"Invalid gear change: {gear[0]}")

                change_gears(car,
                             gear,
                             gears_list)

            if value in ["q", "Q", "", " "]:
                break

        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    run(load_config)
