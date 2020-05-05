# ---------------------------------------------------------------------


from functools import partial


# ---------------------------------------------------------------------


class Proto:
    __functype = type(lambda: None)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.__link = None

    def link(self, other):
        self.__link = other
        return self

    def move(self, other):
        attr = other
        while attr:
            for key in attr.__dict__:
                if key not in self.__dict__:
                    self.__dict__[key] = attr.__dict__[key]
            attr = attr.__link
        return self

    # ---------------------------------------------------------------------

    def __setattr__(self, name, data):
        if self.__functype == type(data):
            data = partial(data, self)

        self.__dict__[name] = data

    def __getattr__(self, name):
        attr = self
        while attr:
            if name in attr.__dict__:
                return attr.__dict__[name]
            attr = attr.__link
        exn = "<proto object at {}> has no attribute '{}'>"
        raise AttributeError(exn.format(hex(id(self)), name))

    # ---------------------------------------------------------------------

    def __str__(self):
        try:
            return self.str()
        except AttributeError:
            return str(self.__dict__)

    def __repr__(self):
        try:
            return self.repr()
        except AttributeError:
            return repr(self.__dict__)

    def __bytes__(self):
        try:
            return self.bytes()
        except AttributeError:
            return bytes(self.__dict__)


"""
mikan = Proto(name='mikan', color='11')
print(mikan.name, mikan.color)
print()

orenji = Proto(name='orenji').link(mikan)
print(orenji.name, orenji.color)
print(mikan.name, mikan.color)
print()

tomato = Proto(name='tomato').move(orenji)
mikan.color = '9'
print(mikan.name, mikan.color)
print(orenji.name, orenji.color)
print(tomato.name, tomato.color)
print()
"""

mikan = Proto(name="mikan", color="11")
print(mikan)

mikan.str = lambda self: "MIKAN!"
print(mikan)