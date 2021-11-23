"""Library for building symbolic expressions.

Extensible combinator library for building symbolic
expressions that can be evaluated at a later time.
"""

from __future__ import annotations
import doctest

class symbol:
    """
    Class for symbol data structure; symbolic expressions are
    trees consisting of nested symbols.
    """
    def __init__(self, instance):
        """
        Create a symbol from an instance (e.g., value, object, or function).

        >>> add = lambda x, y: x + y
        >>> add_ = symbol(add)
        >>> add_.instance(1, 2)
        3
        """
        self.instance = instance
        self.parameters = None

    def __call__(self, *parameters):
        """
        Create a symbolic expression by applying a symbol
        to parameter expressions.

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
        s.parameters = parameters
        return s

    def __getitem__(self, key):
        """
        Allow retrieval of parameters.

        >>> add = lambda x, y: x + y
        >>> add_ = symbol(add)
        >>> e = add_(symbol(1), symbol(2))
        >>> (e[0].instance, e[1].instance)
        (1, 2)
        >>> [e[i].instance for (i, p) in enumerate(e.parameters)]
        [1, 2]
        """
        return self.parameters[key]

    def __iter__(self):
        """
        Allow iteration over parameters.

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

    def __len__(self):
        """
        The length of a symbol instance corresponds to
        the number of parameters it has.

        >>> add = lambda x, y: x + y
        >>> len(symbol(add))
        0
        >>> e = symbol(add)(symbol(1), symbol(2))
        >>> len(e)
        2
        """
        return len(self.parameters) if self.parameters is not None else 0

    def evaluate(self):
        """
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

    def __add__(self, other):
        """
        >>> e = symbol(2) + symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        5
        """
        return add_(self, other)

    def __sub__(self, other):
        """
        >>> e = symbol(2) - symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        -1
        """
        return sub_(self, other)

    def __mul__(self, other):
        """
        >>> e = symbol(2) * symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        6
        """
        return mul_(self, other)


    def __matmul__(self, other):
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

    def __truediv__(self, other):
        """
        >>> e = symbol(5) / symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        2.5
        """
        return div_(self, other)

    def __floordiv__(self, other):
        """
        >>> e = symbol(5) // symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        2
        """
        return floordiv_(self, other)

    def __mod__(self, other):
        """
        >>> e = symbol(5) % symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        1
        """
        return mod_(self, other)

    def __pow__(self, other):
        """
        >>> e = symbol(5) ** symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        25
        """
        return pow_(self, other)

    def __lshift__(self, other):
        """
        >>> e = symbol(4) << symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        16
        """
        return lshift_(self, other)

    def __rshift__(self, other):
        """
        >>> e = symbol(16) >> symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        4
        """
        return rshift_(self, other)

    def __and__(self, other):
        """
        >>> e = symbol({1, 2}) & symbol({2, 3})
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        {2}
        """
        return bitand_(self, other)

    def __xor__(self, other):
        """
        >>> e = symbol({1, 2}) ^ symbol({2, 3})
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        {1, 3}
        """
        return bitxor_(self, other)

    def __or__(self, other):
        """
        >>> e = symbol({1, 2}) | symbol({2, 3})
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        {1, 2, 3}
        """
        return bitor_(self, other)

    def __neg__(self):
        """
        >>> e = -symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        -2
        """
        return neg_(self)

    def __pos__(self):
        """
        >>> e = +symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        2
        """
        return pos_(self)

    def __invert__(self):
        """
        >>> e = ~symbol(2)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        -3
        """
        return invert_(self)

    def __eq__(self, other):
        """
        >>> e = symbol(2) == symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        False
        """
        return eq_(self, other)

    def __ne__(self, other):
        """
        >>> e = symbol(2) != symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        True
        """
        return ne_(self, other)

    def __lt__(self, other):
        """
        >>> e = symbol(2) < symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        True
        """
        return lt_(self, other)

    def __le__(self, other):
        """
        >>> e = symbol(2) <= symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        True
        """
        return le_(self, other)

    def __gt__(self, other):
        """
        >>> e = symbol(2) > symbol(3)
        >>> isinstance(e, symbol)
        True
        >>> e.evaluate()
        False
        """
        return gt_(self, other)

    def __ge__(self, other):
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

def _and_(x, y):
    """
    >>> isinstance(and_(symbol(False), symbol(True)), symbol)
    True
    >>> and_.instance(True, False)
    False
    """
    return x and y
and_ = symbol(_and_)

def _or_(x, y):
    """
    >>> isinstance(or_(symbol(False), symbol(True)), symbol)
    True
    >>> or_.instance(True, False)
    True
    """
    return x or y
or_ = symbol(_or_)

def _add_(x, y):
    """
    >>> isinstance(add_(symbol(2), symbol(3)), symbol)
    True
    >>> add_.instance(2, 3)
    5
    """
    return x + y
add_ = symbol(_add_)

def _sub_(x, y):
    """
    >>> isinstance(sub_(symbol(2), symbol(3)), symbol)
    True
    >>> sub_.instance(2, 3)
    -1
    """
    return x - y
sub_ = symbol(_sub_)

def _mul_(x, y):
    """
    >>> isinstance(mul_(symbol(2), symbol(3)), symbol)
    True
    >>> mul_.instance(2, 3)
    6
    """
    return x * y
mul_ = symbol(_mul_)

def _matmul_(x, y):
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

def _div_(x, y):
    """
    >>> isinstance(div_(symbol(5), symbol(2)), symbol)
    True
    >>> div_.instance(5, 2)
    2.5
    """
    return x / y
div_ = symbol(_div_)
truediv_ = div_ # Synonym based on method names in Python data model.

def _floordiv_(x, y):
    """
    >>> isinstance(floordiv_(symbol(5), symbol(2)), symbol)
    True
    >>> floordiv_.instance(5, 2)
    2
    """
    return x // y
floordiv_ = symbol(_floordiv_)

def _mod_(x, y):
    """
    >>> isinstance(mod_(symbol(5), symbol(2)), symbol)
    True
    >>> mod_.instance(5, 2)
    1
    """
    return x % y
mod_ = symbol(_mod_)

def _pow_(x, y):
    """
    >>> isinstance(pow_(symbol(2), symbol(3)), symbol)
    True
    >>> pow_.instance(2, 3)
    8
    """
    return x ** y
pow_ = symbol(_pow_)

def _lshift_(x, y):
    """
    >>> isinstance(lshift_(symbol(4), symbol(2)), symbol)
    True
    >>> lshift_.instance(4, 2)
    16
    """
    return x << y
lshift_ = symbol(_lshift_)

def _rshift_(x, y):
    """
    >>> isinstance(rshift_(symbol(16), symbol(2)), symbol)
    True
    >>> rshift_.instance(16, 2)
    4
    """
    return x >> y
rshift_ = symbol(_rshift_)

def _bitand_(x, y):
    """
    >>> isinstance(bitand_(symbol({1, 2}), symbol({2, 3})), symbol)
    True
    >>> bitand_.instance({1, 2}, {2, 3})
    {2}
    """
    return x & y
bitand_ = symbol(_bitand_)
amp_ = bitand_ # Concise synonym.

def _bitxor_(x, y):
    """
    >>> isinstance(bitxor_(symbol({1, 2}), symbol({2, 3})), symbol)
    True
    >>> bitxor_.instance({1, 2}, {2, 3})
    {1, 3}
    """
    return x ^ y
bitxor_ = symbol(_bitxor_)
xor_ = bitxor_ # Concise synonym

def _bitor_(x, y):
    """
    >>> isinstance(bitor_(symbol({1, 2}), symbol({2, 3})), symbol)
    True
    >>> bitor_.instance({1, 2}, {2, 3})
    {1, 2, 3}
    """
    return x | y
bitor_ = symbol(_bitor_)
bar_ = bitor_ # Concise synonym.

def _invert_(x):
    """
    >>> isinstance(invert_(symbol(2)), symbol)
    True
    >>> invert_.instance(2)
    -3
    """
    return ~x
invert_ = symbol(_invert_)

def _not_(x):
    """
    >>> isinstance(not_(symbol(True)), symbol)
    True
    >>> not_.instance(True)
    False
    """
    return not x
not_ = symbol(_not_)

def _pos_(x):
    """
    >>> isinstance(pos_(symbol(3)), symbol)
    True
    >>> pos_.instance(3)
    3
    """
    return +x
pos_ = symbol(_pos_)
uadd_ = pos_ # Synonym based on AST module names.

def _neg_(x):
    """
    >>> isinstance(neg_(symbol(3)), symbol)
    True
    >>> neg_.instance(3)
    -3
    """
    return -x
neg_ = symbol(_neg_)
usub_ = neg_ # Synonym based on AST module names.

def _eq_(x, y):
    """
    >>> isinstance(eq_(symbol(3), symbol(2)), symbol)
    True
    >>> eq_.instance(3, 2)
    False
    """
    return x == y
eq_ = symbol(_eq_)

def _ne_(x, y):
    """
    >>> isinstance(ne_(symbol(3), symbol(2)), symbol)
    True
    >>> ne_.instance(3, 2)
    True
    """
    return x != y
ne_ = symbol(_ne_)

def _lt_(x, y):
    """
    >>> isinstance(lt_(symbol(3), symbol(2)), symbol)
    True
    >>> lt_.instance(3, 2)
    False
    """
    return x < y
lt_ = symbol(_lt_)

def _le_(x, y):
    """
    >>> isinstance(le_(symbol(3), symbol(2)), symbol)
    True
    >>> le_.instance(3, 2)
    False
    """
    return x <= y
le_ = symbol(_le_)

def _gt_(x, y):
    """
    >>> isinstance(gt_(symbol(3), symbol(2)), symbol)
    True
    >>> gt_.instance(3, 2)
    True
    """
    return x > y
gt_ = symbol(_gt_)

def _ge_(x, y):
    """
    >>> isinstance(ge_(symbol(3), symbol(2)), symbol)
    True
    >>> ge_.instance(3, 2)
    True
    """
    return x >= y
ge_ = symbol(_ge_)

def _in_(x, y):
    """
    >>> isinstance(in_(symbol(2), symbol({1, 2, 3})), symbol)
    True
    >>> in_.instance(2, {1, 2, 3})
    True
    """
    return x in y
in_ = symbol(_in_)

def _is_(x, y):
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
