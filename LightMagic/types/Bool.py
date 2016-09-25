from ._Base import _Base


class Bool(_Base):
    """
        Работа с bool
    """

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        return bool(value)

    def get_db_type(self):
        return 'bool'
