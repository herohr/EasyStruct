from ByteTypes import *
import struct
import django
import sqlalchemy
class MetaOfStruct(type):
    def __new__(mcs, class_name, parents_name, attrs):
        if class_name == 'BaseStruct':
            return type.__new__(mcs, class_name, parents_name, attrs)

        mapping = {}
        _type_names_set = set()
        _type_names_list = list()
        struct_string = ""
        for key, value in attrs.items():
            if key.startswith("__") or key.startswith("_"):
                continue
            if isinstance(value, BaseBytesType):
                _type_names_set.add(key)
                _type_names_list.append(key)

                struct_string = "".join([struct_string, value.struct_string])
                mapping[key] = value

        # attrs["__getattr__"] = MetaOfStruct.struct_getattr
        attrs["_mapping"] = mapping
        attrs["_type_names_set"] = _type_names_set
        attrs["_type_names_list"] = _type_names_list
        attrs["struct_string"] = struct_string

        return type.__new__(mcs, class_name, parents_name, attrs)

    @staticmethod
    def struct_getattr(self, name):
        if name in self._type_names:
            return self._get_val_of_struct(name)
        else:
            return getattr(self, name)


class BaseStruct(metaclass=MetaOfStruct):
    # @staticmethod
    # def mapping(**kwargs):

    def __init__(self, data=None, order="!", **kwargs):
        self.order = order
        if data is not None:
            self.data = data
            self.unpack()

        for name, val in kwargs.items():
            if name in self._type_names_set:
                setattr(self, name, val)

        # self.struct_string = "".join(*self.)
    # def _get_val_of_struct(self, name):
    #     return self.__getattribute__(name)

    def unpack(self, order=None):
        order = order or self.order
        if self.data:
            result = struct.unpack("{}{}".format(order, self.struct_string), self.data)
            if not len(result) == len(self._type_names_list):
                pass

            for index, name in enumerate(self._type_names_list):
                self.__setattr__(name, result[index])

    def pack(self, order=None):
        order = order or self.order
        return struct.pack("{}{}".format(order, self.struct_string),
                           *[self.__getattribute__(name) for name in self._type_names_list])

    def __len__(self):
        self.data = self.pack()
        if self.data:
            return len(self.data)


class User(BaseStruct):

    name = String(32)
    age = Int()


a = User()
a.name = "fuckyou".encode("utf-8")
a.age = 1
print(a.pack())