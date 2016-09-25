import datetime

from ._Base import _Base


class Date(_Base):
    """
        Работает с датой
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._dayfirst = kwargs.get('dayfirst', False)
        self._yearfirst = kwargs.get('yearfirst', False)

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        if isinstance(value, datetime.datetime):
            return value.date()

        elif isinstance(value, datetime.date):
            return value

        elif isinstance(value, str):
            for format in ('%Y-%m-%d', '%d.%m.%Y'):
                try:
                    return datetime.datetime.strptime(value, format)
                except ValueError:
                    pass

        raise ValueError('Unsupported Format of Value')

    def get_db_type(self):
        if self.db_type:
            return self.db_type
        return 'date'
