import re
import keyword

from collections import OrderedDict


def isidentifier(s, rx=re.compile(r'[a-zA-Z_]\w*')):
    return rx.match(s) is not None and ' ' not in s


class Dict(OrderedDict):
    def __init__(self, items):
        super(Dict, self).__init__(items)

    def __repr__(self):
        return '%s!%s' % (List(*self.keys()), List(*self.values()))


class Atom(object):
    def __init__(self, s):
        assert isinstance(s, (basestring, Symbol, String))
        self.s = getattr(s, 's', s)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return type(self) == type(other) and self.s == other.s

    def __repr__(self):
        return self.s


class String(Atom):
    def __init__(self, s):
        super(String, self).__init__(str(s))

    def __repr__(self):
        return '"%s"' % self.s


class Symbol(Atom):
    def __init__(self, s):
        super(Symbol, self).__init__(s)

    def __getitem__(self, name):
        """
        Examples
        --------
        >>> from kdbpy.compute import q
        >>> t = q.Symbol('t')
        >>> t['s']['a']
        `t.s.a
        """
        return type(self)('%s.%s' % (self.s, name))

    def __repr__(self):
        s = self.s
        if not isidentifier(s) and not keyword.iskeyword(s):
            return '`$%s' % String(s)
        return '`' + s


class List(object):
    def __init__(self, *items):
        self.items = items

    def __repr__(self):
        if len(self) == 1:
            return '(,:[%s])' % self[0]
        return '(%s)' % '; '.join(map(str, self.items))

    def __getitem__(self, key):
        result = self.items[key]
        if isinstance(key, slice):
            return List(*result)
        return result

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __eq__(self, other):
        return type(self) == type(other) and self.items == other.items


class Bool(object):
    def __init__(self, value=False):
        self.value = bool(value)

    def __repr__(self):
        return '%ib' % self.value

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    def __ne__(self, other):
        return not (self == other)


Expr = Dict, Atom, List, Bool