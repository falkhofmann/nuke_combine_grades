
# Import built-in modules
from abc import ABCMeta, abstractmethod
import logging
from math import pow
from cmath import exp
from math import pow

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AbstractNode:
    """Abstract class to represent base node inside nuke."""
    _calculated = None
    _values_in = None
    _parameter = None
    _mix = None

    __metaclass__ = ABCMeta

    def __init__(self, values_in=[1.0, 1.0, 1.0, 1.0], parameter=[1.0, 1.0, 1.0, 1.0], mix=1.0):
        self._values_in = values_in
        self._parameter = parameter
        self._mix = mix
        self.evaluate_values()

    @abstractmethod
    def evaluate_values(self):
        pass

    @property
    def values_out(self):
        return [self._calculated[idx] * self._mix + (self._values_in[idx] * (1.0 - self._mix)) for idx, value in
                enumerate(self._calculated)]


class Add(AbstractNode):
    """Represent an Add node inside nuke within its functionality."""

    def evaluate_values(self):
        self._calculated = [self._values_in[index] + parameter for index, parameter in enumerate(self._parameter)]


class ColorLookup(AbstractNode):

    def evaluate_values(self):
        pass


class Gamma(AbstractNode):
    """Represent a Gamma node inside nuke within its functionality."""

    def evaluate_values(self):
        self._calculated = [1 / pow(1 / self._values_in[index], 1 / parameter) for index, parameter in enumerate(self._parameter)]


class Grade(AbstractNode):
    """Represent a Grade node inside nuke within its functionality."""

    _blackpoint, _whitepoint, _black, _white, _multiply, _add, _gamma = [None for _ in range(7)]

    def __init__(self, values_in, blackpoint, whitepoint, black, white, multiply, add, gamma, mix=1.0):
        self._values_in = values_in
        self._blackpoint = blackpoint
        self._whitepoint = whitepoint
        self._black = black
        self._white = white
        self._multiply = multiply
        self._add = add
        self._gamma = gamma
        self._mix = mix
        self.evaluate_values()

    def evaluate_values(self):
        self._calculated = [self._grade_math(value, idx) for idx, value in enumerate(self._values_in)]

    def _grade_math(self, value, idx):

        first = self._multiply[idx] * (self._white[idx] - self._black[idx]) / (
                self._whitepoint[idx] - self._blackpoint[idx])
        second = self._add[idx] + self._black[idx] - first * self._blackpoint[idx]
        third = first * value + second
        if third <= 0:
            return first * value + second
        return pow((first * value) + second, 1 / self._gamma[idx])


class Multiply(AbstractNode):
    """Represent a Multiply node inside nuke within its functionality."""

    def evaluate_values(self):
        self._calculated = [self._values_in[index] * paramter for index, paramter in enumerate(self._parameter)]
