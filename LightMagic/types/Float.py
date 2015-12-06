from ._Base import _Base


class Float(_Base):
    """
        Работа с float
    """

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        return float(value)
