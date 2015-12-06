class _Base(object):
    """ Базовый класс для типов """

    def __init__(self, value=None, allow_none=True, db_default_value=None, db_primary_key=False, db_autovalue=False, db_type=None):
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

        # Поддержка нескольких объектов одного класса
        self._values_dict = {}

    def __set__(self, obj, value):
        """ Устанавливаем значение """
        self._values_dict[id(obj)] = self.check_value(obj, value)

    def check_value(self, obj, value):
        """ Проверяет, корректно ли значение и проходит ли оно валидацию. """
        self.__validate(obj, value)
        if value is None:
            return value
        else:
            return self._validate(obj, value)

    def __get__(self, obj, objtype):
        """ Возвращает значение """
        return self._values_dict.get(id(obj), self.value)


    def __validate(self, obj, value):
        """ Проверяет корректность входных данных """
        if value is None:
            if self.allow_none is False:
                raise ValueError('None value is not allowed')
            else:
                return value

    @staticmethod
    def get_db_type():
        """ Возвращает тип в БД. Необходимо для сложных типов данных. """
        return None

    @staticmethod
    def db_serialize(value):
        """ Трансформирование объекта в БД. Необходимо для преобразования сложных типов данных. """
        return value

    def __str__(self):
        """ Возвращает вид для отображения """
        return str(self.value)

    @staticmethod
    def db_deserialize(value):
        return value