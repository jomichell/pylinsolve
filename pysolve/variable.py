""" Contains the Variable class.

    Copyright (c) 2014 Kenn Takara
    See LICENSE for details

"""

from sympy import Symbol

from pysolve import InvalidNameError


class Variable(Symbol):
    """ This class contains a 'variable'.  This is a value that
        is being solved here, thus it can change during solving.
        (This is the opposite of a parameter, which is not changed
        by the solver during the solving of a problem).

        Unallowed names are the constants used by sympy:
            I, oo, nan, pi, E

        Attributes:
            name: The symbolic name of the variable.
            desc: A long form description of the variable.
            default: The default value (the initial value of the var)
            model: The model that this variable belongs to.
            value: The actual (current) value of the var.
            equation: This is the equation used to evaluate the
                variable.
    """
    # pylint: disable=too-many-ancestors

    ILLEGAL_NAMES = ['I', 'oo', 'nan', 'pi', 'E']

    def __new__(cls, name, desc=None, default=None):
        if name in Variable.ILLEGAL_NAMES:
            raise InvalidNameError(name, 'Name already used by sympy')

        v = super().__new__(cls, name=name)

        v.name = name
        v.desc = desc
        v.default = default
        v.model = None
        v.equation = None
        v.value = default

        v._index = None

        return v
