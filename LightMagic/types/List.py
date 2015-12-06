from ._Base import _Base


class List(_Base):
    """
        Работа с однотипными массивами.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_value = kwargs['value']
        self.list_type = kwargs['type']
        self.value = []

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных для каждого элемента массива
        """
        if isinstance(value, list):
            for item in value:
                if not isinstance(item, self.list_type):
                    raise ValueError
            return value
        else:
            raise ValueError

    def get_db_type(self):
        return '%s[]' % self.list_type.get_db_type()

    def __add__(self, other):
        if not isinstance(other, self.list_type):
            raise ValueError
        self.value.append(other)

    @staticmethod
    def db_deserialize(value):
        if isinstance(value, str):
            return [x.strip() for x in value.replace('{', '').replace('}', '').split(',')]

        raise ValueError
