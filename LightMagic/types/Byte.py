from ._Base import _Base


class Byte(_Base):
    """
        Работа с байтами
    """

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        return bytes(value)
