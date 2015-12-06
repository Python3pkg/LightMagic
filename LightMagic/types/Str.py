from ._Base import _Base


class Str(_Base):
    """
        Работа с str
    """

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        return str(value)
