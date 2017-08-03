""" Contains the Parameter class.

    Copyright (c) 2014 Kenn Takara
    See LICENSE for details

"""

from sympy import Symbol

from pysolve import InvalidNameError
from pysolve.variable import Variable


class Parameter(Symbol):
    """ This class contains a 'parameter'.  This is an exogenous
        variable.  The solver is not allowed to change this value
        when solving a set of equations.

        Attributes:
            symbol:
            name:
            desc:
            default:
            value:
    """
    # pylint: disable=too-many-ancestors

    def __new__(cls, name, desc=None, default=None):
        if name in Variable.ILLEGAL_NAMES:
            raise InvalidNameError(name, 'Name already used by sympy')

        param = super().__new__(cls, name)
        param.name = name
        param.desc = desc
        param.default = default
        param.model = None

        param._index = None
        param._value = default

        return param

    @property
    def value(self):
        """ Getter accessor for parameter value """
        return self._value

    @value.setter
    def value(self, val):
        """ Setter accessor for parameter value """
        self._value = val


class SeriesParameter(Parameter):
    """ A parameter that can access the previous solution values.

        Attributes:
            name:
            variable:
            iteration:
            default:
    """
    # pylint: disable=too-many-ancestors

    def __new__(cls, name, variable=None, iteration=None, default=None):
        s_param = super().__new__(cls, name, default=default)
        if variable is None or iteration is None:
            raise ValueError('variable and iteration cannot be none')
        s_param.variable = variable
        s_param.iteration = iteration

        return s_param

    @property
    def value(self):
        """ Returns the value of a variable at a another iteration.

            If the iteration value is out-of-range, the variable's
            default value is returned.
        """
        try:
            return self.variable.model.get_value(
                self.variable, self.iteration)
        except IndexError:
            return self.variable.value or self.variable.default
