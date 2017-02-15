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
        try:
            return str(ipaddress.ip_address(value))
        except ValueError:
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