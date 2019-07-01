from abc import ABCMeta, abstractmethod
from decimal import Decimal
import logging
from math import pow

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AbstractNode:
    _calulated = None
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
        return [self._calulated[idx] * self._mix + (self._values_in[idx] * (1.0 - self._mix)) for idx, value in
                enumerate(self._calulated)]


class Add(AbstractNode):

    def evaluate_values(self):
        self._calulated = [self._values_in[idx] + self._parameter[idx] for idx, value in enumerate(self._values_in)]


class ColorLookup(AbstractNode):

    def evaluate_values(self):
        pass


class Gamma(AbstractNode):

    def evaluate_values(self):
        self._calulated = [1/pow(1/self._values_in[idx], 1/self._parameter[idx],) for idx, value in enumerate(self._values_in)]


class Grade(AbstractNode):

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
        self._calulated = [self._grade_math(value, idx) for idx, value in enumerate(self._values_in)]

    def _grade_math(self, value, idx):
        first = self._multiply[idx] * (self._white[idx]-self._black[idx])/(self._whitepoint[idx]-self._blackpoint[idx])
        second = self._add[idx] + self._black[idx] - first * self._blackpoint[idx]
        return pow(first * value + second, 1/self._gamma[idx])


class Multiply(AbstractNode):

    def evaluate_values(self):
        self._calulated = [self._values_in[idx] * self._parameter[idx] for idx, value in enumerate(self._values_in)]


if __name__ == '__main__':


    grade_values_in = [1.0, 1.0, 1.0, 1.0]
    grade = Grade(grade_values_in,
                  [0.0, 0.0, 0.0, 0.0],
                  [1.0, 1.0, 1.0, 1.0],
                  [0.0, 0.0, 0.0, 0.0],
                  [1.0, 1.0, 1.0, 1.0],
                  [1.0, 1.0, 1.0, 1.0],
                  [0.1, 0.2, 0.3, 0.0],
                  [1.1, 1.2, 1.3, 1.0],)

    logger.info('gamma')
    logger.info(grade.values_out)




    multiply_values_in = [1.0, 1.0, 1.0, 1.0]
    multiply = Multiply(values_in=multiply_values_in,
                        parameter=[2.0, 1.5, 1.2, 1.0],
                        mix=0.5)
    logger.info('multiply')
    logger.info(multiply.values_out)

    add_values_in = [1.1, 1.2, 1.3, 1.4]
    add = Add(values_in=add_values_in,
              parameter=[0.9, 0.8, 1.2, 1.0],
              mix=0.8)
    logger.info('add')
    logger.info(add.values_out)

    gamma_values_in = [1.5, 1.5, 1.5, 0.5]
    gamma = Gamma(values_in=gamma_values_in,
                  parameter=[0.5, 0.5, 0.5, 0.5],
                  mix=0.5)

    logger.info('gamma')
    logger.info(gamma.values_out)
