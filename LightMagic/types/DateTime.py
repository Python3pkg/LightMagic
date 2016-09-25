import datetime

import dateutil.parser

from ._Base import _Base


class DateTime(_Base):
    """
        Работает с датой/временем
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
            return value

        elif isinstance(value, datetime.date):
            return value

        elif isinstance(value, str):
            return dateutil.parser.parse(value, dayfirst=self._dayfirst, yearfirst=self._yearfirst)

        else:
            raise ValueError('Unknown format: type: %s  | value: %s' % (type(value), str(value)))

    def get_db_type(self):
        if self.db_type:
            return self.db_type
        return 'timestamp with time zone'
