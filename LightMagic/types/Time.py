import datetime

from ._Base import _Base


class Time(_Base):
    """
        Работает со временем (без даты)
    """

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        if isinstance(value, datetime.datetime):
            return value.time()

        elif isinstance(value, datetime.time):
            return value

        elif isinstance(value, str):
            return datetime.datetime.strptime(value, '%H:%M:%S')

    def get_db_type(self):
        if self.db_type:
            return self.db_type
        return 'time with time zone'
