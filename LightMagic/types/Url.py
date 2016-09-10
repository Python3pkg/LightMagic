from ._Base import _Base


class Url(_Base):
    """
        Работа с str
    """

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        if value is None:
            return None
        else:
            return str(value)
