from ._Base import _Base


class Int(_Base):
    """
        Работа с int
    """

    def __init__(self, min=None, max=None, *args, **kwargs):
        # Максимальное значение
        self.max = max
        # Минимальное значение
        self.min = min

        super().__init__(*args, **kwargs)

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        if self.max is not None and int(value) > self.max:
            raise ValueError('Value is longer than the max')
        if self.min is not None and int(value) < self.min:
            raise ValueError('Value is less than the min')

        return int(value)

    def get_db_type(self):
        if self.db_type:
            return self.db_type
        return 'bigint'
