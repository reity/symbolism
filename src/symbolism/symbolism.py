"""
Extensible combinator library for building symbolic expressions that
can be evaluated at a later time.
"""
from __future__ import annotations
from typing import Any, Union, Iterable
import doctest

class symbol:
    """
    Instances of this class represent individual symbolic values, as well as
    entire symbolic expressions (*i.e.*, trees consisting of nested :obj:`symbol`
    instances are represented using the root instance). A symbolic expression
    involving addition of integers is created in the example below.

    >>> from symbolism import *
    >>> addition = symbol(lambda x, y: x + y)
    >>> summation = addition(symbol(1), symbol(2))

    The expression above can be evaluated at a later time.

    >>> summation.evaluate()
    3

    Instances are compatible with all built-in infix and prefix operators.
    When an operator is applied to one or more instances, a new :obj:`symbol`
    instance is created.

    >>> summation = symbol(1) + symbol(2)
    >>> summation.evaluate()
    3

    Pre-defined constants are also provided for all built-in Python operators.

    >>> conjunction = and_(symbol(True), symbol(False))
    >>> conjunction.evaluate()
    False
    """
    def __init__(self: symbol, instance: Any):
        """
        Create a symbol from an instance (*e.g.*, value, object, or
        function).

        >>> add = lambda x, y: x + y
        >>> add_ = symbol(add)
        >>> add_.instance(1, 2)
        3
        """
        self.instance = instance
        self.parameters = None

    def __call__(self: symbol, *args, **kwargs) -> symbol:
        """
        Allow creation of a symbolic expression via application of a
        :obj:`symbol` instance to zero or more parameter expressions.

        >>> add = lambda x, y: x + y
        >>> add_ = symbol(add)
        >>> e = add_(symbol(1), symbol(2))
        >>> isinstance(e, symbol)
        True
        >>> len(e.parameters)
        2
        >>> e.parameters[0].instance
        1

        Keyword arguments are also supported. However, note that the keywords
        are preserved only in the keys of the ``parameters`` attribute (which in
        this case is instantiated as a dictionary). The indexing method
        :obj:`~symbol.__getitem__` and the iteration method :obj:`~symbol.__iter__`
        only support positional integer indexing and (where applicable) slicing.

        >>> add = lambda x, y: x + y
        >>> add_ = symbol(add)
        >>> e = add_(x=symbol(1), y=symbol(2))
        >>> isinstance(e, symbol)
        True
        >>> len(e.parameters)
        2
        >>> e.parameters['x'].instance
        1

        Positional and keyword arguments cannot be mixed.

        >>> add = lambda x, y: x + y
        >>> add_ = symbol(add)
        >>> e = add_(symbol(1), y=symbol(2))
        Traceback (most recent call last):
          ...
        ValueError: cannot mix positional and keyword arguments
        """
        if len(args) > 0 and len(kwargs) > 0:
            raise ValueError('cannot mix positional and keyword arguments')

        s = symbol(self.instance)
        s.parameters = args if len(kwargs) == 0 else kwargs
        return s

    def __getitem__(self: symbol, key: Union[int, slice]) -> Union[Any, list, tuple]:
        """
        Retrieve an instance parameter using an integer index, or retrieve a
        sequence of instance parameters using a slice.

        >>> add = lambda x, y: x + y
        >>> add_ = symbol(add)
        >>> e = add_(symbol(1), symbol(2))
        >>> (e[0].instance, e[1].instance)
        (1, 2)
        >>> [e[i].instance for (i, p) in enumerate(e.parameters)]
        [1, 2]
        >>> [e[i].instance for (i, p) in enumerate(e)]
        [1, 2]

        Slice notation is also supported when the ``parameters``
        attribute supports it.

        >>> [s.instance for s in e[0:2]]
        [1, 2]
        """
        return (
            list(self.parameters.values())[key] # pylint: disable=no-member
            if isinstance(self.parameters, dict) else
            self.parameters[key] # Should be a :obj:`tuple`; see :obj:`__init__`.
        )

    def __iter__(self: symbol) -> Iterable:
        """
        Allow iteration over instance parameters.

        >>> add = lambda x, y: x + y
        >>> add_ = symbol(add)
        >>> e = add_(symbol(1), symbol(2))
        >>> [p.instance for p in e]
        [1, 2]
        >>> 123 in add_(123)
        True

        Even if keyword arguments are used when this instance is instantiated,
        the iteration returns the actual parameter instances (and **not** the
        keys of the ``parameters`` attribute).

        >>> add = lambda x, y: x + y
        >>> add_ = symbol(add)
        >>> e = add_(x=symbol(1), y=symbol(2))
        >>> [p.instance for p in e]
        [1, 2]
        >>> 123 in add_(123)
        True
        """
        for parameter in (
            self.parameters.values() # pylint: disable=no-member
            if isinstance(self.parameters, dict) else
            self.parameters
        ):
            yield parameter

    def __len__(self: symbol) -> int:
        """
        The length of an instance corresponds to the number of parameters that
        it has.

        >>> add = lambda x, y: x + y
        >>> len(symbol(add))
        0
        >>> e = symbol(add)(symbol(1), symbol(2))
        >>> len(e)
        2
        """
        return len(self.parameters) if self.parameters is not None else 0

    def evaluate(self: symbol) -> Any:
        """
        Evaluate a symbolic expression (via recursive evaluation of all
        subexpressions) and return the result.

        >>> add = lambda x, y: x + y
        >>> e = symbol(add)(symbol(1), symbol(2))
        >>> e.evaluate()
        3
        >>> e = symbol(list.__getitem__)(symbol(['a', 'b', 'c']), symbol(1))
        >>> e.evaluate()
        'b'
        """
        if self.parameters is None:
            return self.instance

        return self.instance(*[
            parameter.evaluate()
            for parameter in (
                self.parameters.values() # pylint: disable=no-member
                if isinstance(self.parameters, dict) else
                self.parameters
            )
        ])

    def __add__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(2) + symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        5
        """
        return add_(self, other)

    def __sub__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(2) - symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        -1
        """
        return sub_(self, other)

    def __mul__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(2) * symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        6
        """
        return mul_(self, other)


    def __matmul__(self: symbol, other: symbol) -> symbol:
        """
        >>> class Test:
        ...     def __matmul__(self, other):
        ...         return True
        >>> e = symbol(Test()) @ symbol(Test())
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        True
        """
        return matmul_(self, other)

    def __truediv__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(5) / symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        2.5
        """
        return div_(self, other)

    def __floordiv__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(5) // symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        2
        """
        return floordiv_(self, other)

    def __mod__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(5) % symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        1
        """
        return mod_(self, other)

    def __pow__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(5) ** symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        25
        """
        return pow_(self, other)

    def __lshift__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(4) << symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        16
        """
        return lshift_(self, other)

    def __rshift__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(16) >> symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        4
        """
        return rshift_(self, other)

    def __and__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol({1, 2}) & symbol({2, 3})
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        {2}
        """
        return bitand_(self, other)

    def __xor__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol({1, 2}) ^ symbol({2, 3})
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        {1, 3}
        """
        return bitxor_(self, other)

    def __or__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol({1, 2}) | symbol({2, 3})
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        {1, 2, 3}
        """
        return bitor_(self, other)

    def __neg__(self: symbol) -> symbol:
        """
        >>> e = -symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        -2
        """
        return neg_(self)

    def __pos__(self: symbol) -> symbol:
        """
        >>> e = +symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        2
        """
        return pos_(self)

    def __invert__(self: symbol) -> symbol:
        """
        >>> e = ~symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        -3
        """
        return invert_(self)

    def __eq__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(2) == symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        False
        """
        return eq_(self, other)

    def __ne__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(2) != symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        True
        """
        return ne_(self, other)

    def __lt__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(2) < symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        True
        """
        return lt_(self, other)

    def __le__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(2) <= symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        True
        """
        return le_(self, other)

    def __gt__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(2) > symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        False
        """
        return gt_(self, other)

    def __ge__(self: symbol, other: symbol) -> symbol:
        """
        >>> e = symbol(2) >= symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        False
        """
        return ge_(self, other)

# In order to accommodate the limitations of measuring coverage of unit tests,
# the @symbol decorator is not used in the definitions below.

def _and_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(and_(symbol(False), symbol(True)), symbol)
    True
    >>> and_.instance(True, False)
    False
    """
    return x and y

and_ = symbol(_and_)
"""
.. |and| replace:: ``and``
.. _and: https://docs.python.org/3/reference/expressions.html#boolean-operations

Symbolic function corresponding to the infix boolean operator |and|_.
"""

def _or_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(or_(symbol(False), symbol(True)), symbol)
    True
    >>> or_.instance(True, False)
    True
    """
    return x or y

or_ = symbol(_or_)
"""
.. |or| replace:: ``or``
.. _or: https://docs.python.org/3/reference/expressions.html#boolean-operations

Symbolic function corresponding to the infix boolean operator |or|_.
"""

def _not_(x: symbol) -> symbol:
    """
    >>> isinstance(not_(symbol(True)), symbol)
    True
    >>> not_.instance(True)
    False
    """
    return not x

not_ = symbol(_not_)
"""
.. |not| replace:: ``not``
.. _not: https://docs.python.org/3/reference/expressions.html#boolean-operations

Symbolic function corresponding to the prefix boolean operator |not|_.
"""

def _in_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(in_(symbol(2), symbol({1, 2, 3})), symbol)
    True
    >>> in_.instance(2, {1, 2, 3})
    True
    """
    return x in y

in_ = symbol(_in_)
"""
.. |in| replace:: ``in``
.. _in: https://docs.python.org/3/reference/expressions.html#comparisons

Symbolic function corresponding to the infix operator |in|_.
"""

def _is_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(is_(symbol(2), symbol(2)), symbol)
    True
    >>> is_.instance(2, 2)
    True
    """
    return x is y

is_ = symbol(_is_)
"""
.. |is| replace:: ``is``
.. _is: https://docs.python.org/3/reference/expressions.html#comparisons

Symbolic function corresponding to the infix operator |is|_.
"""

def _add_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(add_(symbol(2), symbol(3)), symbol)
    True
    >>> add_.instance(2, 3)
    5
    """
    return x + y

add_ = symbol(_add_)
"""Alias for :obj:`symbol.__add__`."""

def _sub_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(sub_(symbol(2), symbol(3)), symbol)
    True
    >>> sub_.instance(2, 3)
    -1
    """
    return x - y

sub_ = symbol(_sub_)
"""Alias for :obj:`symbol.__sub__`."""

def _mul_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(mul_(symbol(2), symbol(3)), symbol)
    True
    >>> mul_.instance(2, 3)
    6
    """
    return x * y

mul_ = symbol(_mul_)
"""Alias for :obj:`symbol.__mul__`."""

def _matmul_(x: symbol, y: symbol) -> symbol:
    """
    >>> class Test:
    ...     def __matmul__(self, other):
    ...         return True
    >>> isinstance(matmul_(symbol(Test()), symbol(Test())), symbol)
    True
    >>> matmul_.instance(Test(), Test())
    True
    """
    return x @ y

matmul_ = symbol(_matmul_)
"""Alias for :obj:`symbol.__matmul__`."""

def _div_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(div_(symbol(5), symbol(2)), symbol)
    True
    >>> div_.instance(5, 2)
    2.5
    """
    return x / y

truediv_ = symbol(_div_)
"""Alias for :obj:`symbol.__truediv__`."""

div_ = truediv_
"""Concise alias for :obj:`symbol.__truediv__`."""

def _floordiv_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(floordiv_(symbol(5), symbol(2)), symbol)
    True
    >>> floordiv_.instance(5, 2)
    2
    """
    return x // y

floordiv_ = symbol(_floordiv_)
"""Alias for :obj:`symbol.__floordiv__`."""

def _mod_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(mod_(symbol(5), symbol(2)), symbol)
    True
    >>> mod_.instance(5, 2)
    1
    """
    return x % y

mod_ = symbol(_mod_)
"""Alias for :obj:`symbol.__mod__`."""

def _pow_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(pow_(symbol(2), symbol(3)), symbol)
    True
    >>> pow_.instance(2, 3)
    8
    """
    return x ** y

pow_ = symbol(_pow_)
"""Alias for :obj:`symbol.__pow__`."""

def _lshift_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(lshift_(symbol(4), symbol(2)), symbol)
    True
    >>> lshift_.instance(4, 2)
    16
    """
    return x << y

lshift_ = symbol(_lshift_)
"""Alias for :obj:`symbol.__lshift__`."""

def _rshift_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(rshift_(symbol(16), symbol(2)), symbol)
    True
    >>> rshift_.instance(16, 2)
    4
    """
    return x >> y

rshift_ = symbol(_rshift_)
"""Alias for :obj:`symbol.__rshift__`."""

def _bitand_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(bitand_(symbol({1, 2}), symbol({2, 3})), symbol)
    True
    >>> bitand_.instance({1, 2}, {2, 3})
    {2}
    """
    return x & y

bitand_ = symbol(_bitand_)
"""Alias for :obj:`symbol.__and__`."""

amp_ = bitand_
"""Concise alias for :obj:`symbol.__and__`."""

def _bitxor_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(bitxor_(symbol({1, 2}), symbol({2, 3})), symbol)
    True
    >>> bitxor_.instance({1, 2}, {2, 3})
    {1, 3}
    """
    return x ^ y

bitxor_ = symbol(_bitxor_)
"""Alias for :obj:`symbol.__xor__`."""

xor_ = bitxor_ # Concise synonym
"""Concise alias for :obj:`symbol.__xor__`."""

def _bitor_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(bitor_(symbol({1, 2}), symbol({2, 3})), symbol)
    True
    >>> bitor_.instance({1, 2}, {2, 3})
    {1, 2, 3}
    """
    return x | y

bitor_ = symbol(_bitor_)
"""Alias for :obj:`symbol.__or__`."""

bar_ = bitor_
"""Concise alias for :obj:`symbol.__or__`."""

def _invert_(x: symbol) -> symbol:
    """
    >>> isinstance(invert_(symbol(2)), symbol)
    True
    >>> invert_.instance(2)
    -3
    """
    return ~x

invert_ = symbol(_invert_)
"""Alias for :obj:`symbol.__invert__`."""

def _pos_(x: symbol) -> symbol:
    """
    >>> isinstance(pos_(symbol(3)), symbol)
    True
    >>> pos_.instance(3)
    3
    """
    return +x

pos_ = symbol(_pos_)
"""Alias for :obj:`symbol.__pos__`."""

uadd_ = pos_
"""Alias for :obj:`symbol.__pos__` (alluding to the name of :obj:`ast.UAdd`)."""

def _neg_(x: symbol) -> symbol:
    """
    >>> isinstance(neg_(symbol(3)), symbol)
    True
    >>> neg_.instance(3)
    -3
    """
    return -x

neg_ = symbol(_neg_)
"""Alias for :obj:`symbol.__neg__`."""

usub_ = neg_
"""Alias for :obj:`symbol.__neg__` (alluding to the name of :obj:`ast.USub`)."""

def _eq_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(eq_(symbol(3), symbol(2)), symbol)
    True
    >>> eq_.instance(3, 2)
    False
    """
    return x == y

eq_ = symbol(_eq_)
"""Alias for :obj:`symbol.__eq__`."""

def _ne_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(ne_(symbol(3), symbol(2)), symbol)
    True
    >>> ne_.instance(3, 2)
    True
    """
    return x != y

ne_ = symbol(_ne_)
"""Alias for :obj:`symbol.__ne__`."""

def _lt_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(lt_(symbol(3), symbol(2)), symbol)
    True
    >>> lt_.instance(3, 2)
    False
    """
    return x < y

lt_ = symbol(_lt_)
"""Alias for :obj:`symbol.__lt__`."""

def _le_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(le_(symbol(3), symbol(2)), symbol)
    True
    >>> le_.instance(3, 2)
    False
    """
    return x <= y

le_ = symbol(_le_)
"""Alias for :obj:`symbol.__le__`."""

def _gt_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(gt_(symbol(3), symbol(2)), symbol)
    True
    >>> gt_.instance(3, 2)
    True
    """
    return x > y

gt_ = symbol(_gt_)
"""Alias for :obj:`symbol.__gt__`."""

def _ge_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(ge_(symbol(3), symbol(2)), symbol)
    True
    >>> ge_.instance(3, 2)
    True
    """
    return x >= y

ge_ = symbol(_ge_)
"""Alias for :obj:`symbol.__ge__`."""

if __name__ == '__main__':
    doctest.testmod() # pragma: no cover
