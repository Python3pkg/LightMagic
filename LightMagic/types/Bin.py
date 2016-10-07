import re

from ._Base import _Base


class Bin(_Base):
    """
        Работа с int
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """

        if not re.match('(:?4|5)\d{5}', str(value)):
            raise ValueError('Value isn\'t BIN')

        return int(value)
