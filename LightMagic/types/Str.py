from ._Base import _Base


class Str(_Base):
    """
        Работа с str
    """

    def __init__(self, regexp=None, min_length=None, max_length=None, *args, **kwargs):
        # Регулярное выражение
        self.regexp = regexp
        # Максимальная длина
        self.max_length = max_length
        # Минимальная длина
        self.min_length = min_length
        super().__init__(*args, **kwargs)

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        if self.regexp is not None and not self.regexp.match(value):
            raise ValueError('String does not match rule')
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError('String is longer than the maximum length (%s symbols)' % self.max_length)
        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError('String is less than the minimum length (%s symbols)' % self.min_length)
        if value is None:
            return None
        else:
            return str(value)

    def get_db_type(self):
        if self.db_type:
            return self.db_type
        return 'text'
