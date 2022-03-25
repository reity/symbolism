"""
Extensible combinator library for building symbolic expressions that
can be evaluated at a later time.
"""
from __future__ import annotations
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

    Pre-defined constants are also provided for all built-in operators.

    >>> conjunction = and_(symbol(True), symbol(False))
    >>> conjunction.evaluate()
    False
    """
    def __init__(self: symbol, instance):
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
        """
        s = symbol(self.instance)
        s.parameters = {i: v for i, v in enumerate(*args)} | kwargs
        return s

    def __getitem__(self: symbol, key):
        """
        Retrieve an instance parameter using its index or key.

        >>> add = lambda x, y: x + y
        >>> add_ = symbol(add)
        >>> e = add_(symbol(1), symbol(2))
        >>> (e[0].instance, e[1].instance)
        (1, 2)
        >>> [e[i].instance for (i, p) in enumerate(e.parameters)]
        [1, 2]

        Slice notation is also supported when the ``parameters``
        attribute supports it.

        >>> [s.instance for s in e[0:2]]
        [1, 2]
        """
        return self.parameters[key]

    def __iter__(self: symbol):
        """
        Allow iteration over instance parameters.

        >>> add = lambda x, y: x + y
        >>> add_ = symbol(add)
        >>> e = add_(symbol(1), symbol(2))
        >>> [p.instance for p in e]
        [1, 2]
        >>> 123 in add_(123)
        True
        """
        for parameter in self.parameters:
            yield parameter

    def __len__(self: symbol) -> int:
        """
        The length of an instance corresponds to the number of parameters it
        has.

        >>> add = lambda x, y: x + y
        >>> len(symbol(add))
        0
        >>> e = symbol(add)(symbol(1), symbol(2))
        >>> len(e)
        2
        """
        return len(self.parameters) if self.parameters is not None else 0

    def evaluate(self: symbol):
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

        return self.instance(*[p.evaluate() for p in self.parameters])

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

# In order to accommodate the limitations of measuring
# coverage of unit tests, the @symbol decorator is not
# used in the definitions below.

def _and_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(and_(symbol(False), symbol(True)), symbol)
    True
    >>> and_.instance(True, False)
    False
    """
    return x and y
and_ = symbol(_and_)

def _or_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(or_(symbol(False), symbol(True)), symbol)
    True
    >>> or_.instance(True, False)
    True
    """
    return x or y
or_ = symbol(_or_)

def _add_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(add_(symbol(2), symbol(3)), symbol)
    True
    >>> add_.instance(2, 3)
    5
    """
    return x + y
add_ = symbol(_add_)

def _sub_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(sub_(symbol(2), symbol(3)), symbol)
    True
    >>> sub_.instance(2, 3)
    -1
    """
    return x - y
sub_ = symbol(_sub_)

def _mul_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(mul_(symbol(2), symbol(3)), symbol)
    True
    >>> mul_.instance(2, 3)
    6
    """
    return x * y
mul_ = symbol(_mul_)

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

def _div_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(div_(symbol(5), symbol(2)), symbol)
    True
    >>> div_.instance(5, 2)
    2.5
    """
    return x / y
div_ = symbol(_div_)
truediv_ = div_ # Synonym based on method names in Python data model.

def _floordiv_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(floordiv_(symbol(5), symbol(2)), symbol)
    True
    >>> floordiv_.instance(5, 2)
    2
    """
    return x // y
floordiv_ = symbol(_floordiv_)

def _mod_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(mod_(symbol(5), symbol(2)), symbol)
    True
    >>> mod_.instance(5, 2)
    1
    """
    return x % y
mod_ = symbol(_mod_)

def _pow_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(pow_(symbol(2), symbol(3)), symbol)
    True
    >>> pow_.instance(2, 3)
    8
    """
    return x ** y
pow_ = symbol(_pow_)

def _lshift_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(lshift_(symbol(4), symbol(2)), symbol)
    True
    >>> lshift_.instance(4, 2)
    16
    """
    return x << y
lshift_ = symbol(_lshift_)

def _rshift_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(rshift_(symbol(16), symbol(2)), symbol)
    True
    >>> rshift_.instance(16, 2)
    4
    """
    return x >> y
rshift_ = symbol(_rshift_)

def _bitand_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(bitand_(symbol({1, 2}), symbol({2, 3})), symbol)
    True
    >>> bitand_.instance({1, 2}, {2, 3})
    {2}
    """
    return x & y
bitand_ = symbol(_bitand_)
amp_ = bitand_ # Concise synonym.

def _bitxor_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(bitxor_(symbol({1, 2}), symbol({2, 3})), symbol)
    True
    >>> bitxor_.instance({1, 2}, {2, 3})
    {1, 3}
    """
    return x ^ y
bitxor_ = symbol(_bitxor_)
xor_ = bitxor_ # Concise synonym

def _bitor_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(bitor_(symbol({1, 2}), symbol({2, 3})), symbol)
    True
    >>> bitor_.instance({1, 2}, {2, 3})
    {1, 2, 3}
    """
    return x | y
bitor_ = symbol(_bitor_)
bar_ = bitor_ # Concise synonym.

def _invert_(x: symbol) -> symbol:
    """
    >>> isinstance(invert_(symbol(2)), symbol)
    True
    >>> invert_.instance(2)
    -3
    """
    return ~x
invert_ = symbol(_invert_)

def _not_(x: symbol) -> symbol:
    """
    >>> isinstance(not_(symbol(True)), symbol)
    True
    >>> not_.instance(True)
    False
    """
    return not x
not_ = symbol(_not_)

def _pos_(x: symbol) -> symbol:
    """
    >>> isinstance(pos_(symbol(3)), symbol)
    True
    >>> pos_.instance(3)
    3
    """
    return +x
pos_ = symbol(_pos_)
uadd_ = pos_ # Synonym based on AST module names.

def _neg_(x: symbol) -> symbol:
    """
    >>> isinstance(neg_(symbol(3)), symbol)
    True
    >>> neg_.instance(3)
    -3
    """
    return -x
neg_ = symbol(_neg_)
usub_ = neg_ # Synonym based on AST module names.

def _eq_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(eq_(symbol(3), symbol(2)), symbol)
    True
    >>> eq_.instance(3, 2)
    False
    """
    return x == y
eq_ = symbol(_eq_)

def _ne_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(ne_(symbol(3), symbol(2)), symbol)
    True
    >>> ne_.instance(3, 2)
    True
    """
    return x != y
ne_ = symbol(_ne_)

def _lt_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(lt_(symbol(3), symbol(2)), symbol)
    True
    >>> lt_.instance(3, 2)
    False
    """
    return x < y
lt_ = symbol(_lt_)

def _le_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(le_(symbol(3), symbol(2)), symbol)
    True
    >>> le_.instance(3, 2)
    False
    """
    return x <= y
le_ = symbol(_le_)

def _gt_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(gt_(symbol(3), symbol(2)), symbol)
    True
    >>> gt_.instance(3, 2)
    True
    """
    return x > y
gt_ = symbol(_gt_)

def _ge_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(ge_(symbol(3), symbol(2)), symbol)
    True
    >>> ge_.instance(3, 2)
    True
    """
    return x >= y
ge_ = symbol(_ge_)

def _in_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(in_(symbol(2), symbol({1, 2, 3})), symbol)
    True
    >>> in_.instance(2, {1, 2, 3})
    True
    """
    return x in y
in_ = symbol(_in_)

def _is_(x: symbol, y: symbol) -> symbol:
    """
    >>> isinstance(is_(symbol(2), symbol(2)), symbol)
    True
    >>> is_.instance(2, 2)
    True
    """
    return x is y
is_ = symbol(_is_)

if __name__ == "__main__":
    doctest.testmod() # pragma: no cover
