class _Base(object):
    """ Базовый класс для типов """

    def __init__(self, value=None, allow_none=True, db_default_value=None, db_primary_key=False, db_autovalue=False,
                 db_type=None, db_force_set_primary_key=False, label=None):
        """
        :param value: Значение атрибута по-умолчанию
        :param allow_none: Разрешено ли None значение
        :param default_db_value: Если значение не было установлено, что будет подставлено в БД. Удобно для даты создания объекта.
        :return:
        """
        self.value = value
        self.allow_none = bool(allow_none)
        self.db_default_value = db_default_value
        self.db_primary_key = db_primary_key
        self.db_autovalue = db_autovalue
        self.db_force_set_primary_key = db_force_set_primary_key
        self.db_type = db_type

        self.label = label

        # Поддержка нескольких объектов одного класса
        self._values_dict = {}

    def __set__(self, obj, value):
        """ Устанавливаем значение """
        try:
            obj._light_magic_values[id(self)] = self._pack_value(self.check_value(obj, value))
        except AttributeError:
            obj._light_magic_values = {id(self): self._pack_value(self.check_value(obj, value))}

    def check_value(self, obj, value):
        """ Проверяет, корректно ли значение и проходит ли оно валидацию. """
        self.__validate(obj, value)
        if value is None:
            return value
        else:
            return self._validate(obj, value)

    def __get__(self, obj, objtype):
        """ Возвращает значение """
        try:
            return self._unpack_value(obj._light_magic_values.get(id(self), self.value))
        except AttributeError:
            return self.value

    def __validate(self, obj, value):
        """ Проверяет корректность входных данных """
        if value is None:
            if self.allow_none is False:
                raise ValueError('None value is not allowed')

    def get_db_type(self):
        """ Возвращает тип в БД. Необходимо для сложных типов данных. """
        return None

    def _pack_value(self, value):
        """ Запаковывает значение для внутреннего хранения """
        return value

    def _unpack_value(self, value):
        """ Распаковывает значение для представления """
        return value

    def db_serialize(self, value):
        """ Трансформирование объекта в БД. Необходимо для преобразования сложных типов данных. """
        return value

    def __str__(self):
        """ Возвращает вид для отображения """
        return str(self.value)

    def __repr__(self):
        """ Возвращает вид для отображения """
        return str(self.value)

    def db_deserialize(self, value):
        return value
