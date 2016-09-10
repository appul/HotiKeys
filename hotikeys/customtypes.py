from enum import EnumMeta, Enum


class FlagsDword(int):
    def __iter__(self):
        for k, v in vars(self.__class__).items():
            if isinstance(v, property):
                yield k, getattr(self, k)

    def __contains__(self, flag_name):
        if not isinstance(flag_name, str):
            raise TypeError('expected str'
                            ' for flag name, got {0}'.format(type(flag_name)))
        return flag_name in vars(self.__class__)

    def __getitem__(self, bit):
        if not isinstance(bit, int):
            raise TypeError('expected int'
                            ' for bit, got {0}'.format(type(bit)))
        return bool(self & 2 ** bit)

    # noinspection PyTypeChecker
    def __str__(self):
        return '<{cls}: {binary}>'.format(
                cls=self.__class__.__name__,
                binary=bin(self).split('b')[1]
        )


class IEnumMeta(EnumMeta):
    def __getitem__(cls, item) -> 'IEnumMeta':
        if item in cls.__members__:
            return super().__getitem__(item)
        for enum in cls:
            if enum.value == item:
                return enum
        return None


class IEnum(Enum, metaclass=IEnumMeta):
    def __int__(self):
        if self.value is None:
            return 0
        return int(self.value)

    def __bool__(self):
        return bool(self.value)
