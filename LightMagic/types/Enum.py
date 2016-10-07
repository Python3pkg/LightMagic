from ._Base import _Base


class Enum(_Base):
    """
        Работа с str
    """

    def __init__(self, list_of_values=None, *args, **kwargs):
        # Список допустимых значений
        self.list_of_values = list_of_values

        super().__init__(*args, **kwargs)

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        if value not in self.list_of_values:
            raise ValueError('Invalid value "%s"' % value)

        return value

    def get_db_type(self):
        if self.db_type:
            return self.db_type
        return 'text'
