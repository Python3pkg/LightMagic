from ._Base import _Base


class Int(_Base):
    """
        Работа с int
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __get__(self, *args, **kwargs):
        return super().__get__(*args, **kwargs)

    def __set__(self, *args, **kwargs):
        return super().__set__(*args, **kwargs)

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        return int(value)
