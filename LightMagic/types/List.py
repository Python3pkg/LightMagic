from ._Base import _Base


class List(_Base):
    """
        Работа с однотипными массивами.
    """

    def __init__(self, type_of_elements, db_type=None, value=None, *args, **kwargs):
        self.db_type = db_type
        self.list_type = type_of_elements

        self.default_value = value

        super().__init__(value=None, db_type=db_type, *args, **kwargs)

    def __set__(self, obj, value):
        """ Устанавливаем значение """
        self.default_value = None

        if value is not None:
            if isinstance(self.list_type, _Base):
                value = [self.list_type(value=item) for item in value]
            else:
                value = [self.list_type(item) for item in value]
            super().__set__(obj, value)

    def __get__(self, instance, owner):
        if self.default_value is not None:
            return self.default_value
        else:
            value = super().__get__(instance, owner)
            if value is None:
                super().__set__(instance, [])
                return super().__get__(instance, owner)
            return value

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных для каждого элемента массива
        """
        if isinstance(value, list):
            for item in value:
                if not isinstance(item, self.list_type):
                    raise ValueError('Bad item type')
        else:
            if not isinstance(value, self.list_type):
                raise ValueError('Bad object type')
        return value

    def get_db_type(self):
        return '%s[]' % self.db_type

    def db_serialize(self, value):
        """ Трансформирование объекта в БД. Необходимо для преобразования сложных типов данных. """
        if issubclass(self.list_type, _Base):
            return [self.list_type.db_serialize(x) for x in value]
        return value

    def db_deserialize(self, value):
        """ Разбираем объект из БД """
        if isinstance(value, str):
            value = value.replace('{', '').replace('}', '').strip()
            if len(value) == 0:
                return []
            value = [x.strip() for x in value.split(',')]
            if isinstance(self.list_type, _Base):
                return [self.list_type(value=item) for item in value]
            else:
                return [self.list_type(item) for item in value]

        elif isinstance(value, list):
            return value

        raise ValueError('Can`t deserialize object')

    def append(self, p_object):
        print(self.value)
        self.value.append(self._validate(None, p_object))
        print(self.value)
