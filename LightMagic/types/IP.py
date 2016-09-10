import re
import ipaddress

from ._Base import _Base


class IP(_Base):
    """
        Работа с IP
    """

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        if value in ('::1',):
            return value
        if re.match('(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}', value):
            return str(ipaddress.ip_network(value))
        elif re.match('(?:\d{1,3}\.){3}\d{1,3}', value):
            return str(ipaddress.ip_address(value))
        else:
            raise ValueError('Bad ip format: %s' % value)

    def __str__(self):
        """ Возвращает вид для отображения """
        return str(self.value)

    @staticmethod
    def db_serialize(value):
        """ Трансформирование объекта в БД. Необходимо для преобразования сложных типов данных. """
        if value is None:
            return None
        else:
            return str(value)