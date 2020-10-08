from typing import Any, List, Callable

import os
import time
import gpio
import logging


def load_boolean_environ(name: str) -> bool:
    value = os.environ.get(name, "false").lower()
    return value in ["true", "1", "enabled"]


def load_float_environ(name: str, default: float) -> float:
    return float(os.environ.get(name, default))


def load_list_environ(
    name: str, formatter: Callable[[str], Any], default: List[Any]
) -> List[Any]:
    if name in os.environ:
        value = os.environ.get(name)
        return list(map(formatter, value.split(",")))
    return default


BALENA = load_boolean_environ("BALENA")
INITIAL_STATE = load_boolean_environ("INITIAL_STATE")
DRIVEN_STATE = load_boolean_environ("DRIVEN_STATE")
SLEEP_DELAY = load_float_environ("SLEEP_DELAY", 1)
GPIO_PINS = load_list_environ("GPIO_PINS", int, [5, 6, 8, 9, 11, 16, 20, 23, 24, 25])

logger = logging.getLogger(__name__)


class MockGPIO:
    IN = "IN"
    OUT = "OUT"

    def setup(self, pin, mode, initial=False):
        pass

    def output(self, pin, value):
        pass


if not BALENA:
    logger.warning("using mock gpio")
    gpio = MockGPIO()


def main():
    for gpio_pin in GPIO_PINS:
        logger.info("setup output pin %s with state %s", gpio_pin, INITIAL_STATE)
        gpio.setup(gpio_pin, gpio.OUT, initial=INITIAL_STATE)
        time.sleep(SLEEP_DELAY)
        logger.info("drive output pin %s to state %s", gpio_pin, DRIVEN_STATE)
        gpio.output(gpio_pin, DRIVEN_STATE)
        time.sleep(SLEEP_DELAY)
    while True:
        logger.info("main script complete now sleep forever")
        time.sleep(60 * 5)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()