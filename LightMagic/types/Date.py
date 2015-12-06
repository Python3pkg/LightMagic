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
            self._value = value.date()

        elif isinstance(value, datetime.date):
            self._value = value

        elif isinstance(value, str):
            try:
                self._value = datetime.datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                pass

            self._value = datetime.datetime.strptime(value, '%Y-%m-%d')
        else:
            raise ValueError
