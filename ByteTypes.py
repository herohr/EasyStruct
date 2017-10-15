class MetaOfBytesType(type):
    def __new__(mcs, class_name, parents_class, attrs):
        struct_char = attrs.get("struct_char")
        unit_size = attrs.get("unit_size")
        if class_name == "BaseBytesType":
            return type.__new__(mcs, class_name, parents_class, attrs)

        if not struct_char:
            raise MetaClassError("Class {} must have 'struct_char'".format(class_name))
        if not unit_size:
            raise MetaClassError("Class {} must have 'unit_size'".format(class_name))

        return type.__new__(mcs, class_name, parents_class, attrs)


class MetaClassError(BaseException):
    pass


class BaseBytesType(metaclass=MetaOfBytesType):
    struct_char = None
    unit_size = None
    struct_string = None

    def __init__(self, amount=1):
        self.amount = amount

    def __len__(self):
        return self.unit_size * self.amount

    @property
    def struct_string(self):
        return "{}{}".format(self.amount, self.struct_char)


class Char(BaseBytesType):
    struct_char = 'c'
    unit_size = 1


class SChar(BaseBytesType):
    struct_char = 'b'
    unit_size = 1


class UChar(BaseBytesType):
    struct_char = 'B'
    unit_size = 1


class Bool(BaseBytesType):
    struct_char = "?"
    unit_size = 1


class Short(BaseBytesType):
    struct_char = "h"
    unit_size = 2


class UShort(BaseBytesType):
    struct_char = 'H'
    unit_size = 2


class Int(BaseBytesType):
    struct_char = 'i'
    unit_size = 4


class UInt(BaseBytesType):
    struct_char = 'I'
    unit_size = 4


class Long(BaseBytesType):
    struct_char = 'l'
    unit_size = 4


class ULong(BaseBytesType):
    struct_char = 'L'
    unit_size = 4


class LongLong(BaseBytesType):
    struct_char = "q"
    unit_size = 8


class ULongLong(BaseBytesType):
    struct_char = 'Q'
    unit_size = 8


class Float(BaseBytesType):
    struct_char = 'f'
    unit_size = 4


class Double(BaseBytesType):
    struct_char = 'd'
    unit_size = 8


class String(BaseBytesType):
    struct_char = 's'
    unit_size = 1

if __name__ == "__main__":
    a = String(32)
    print(a.struct_string)