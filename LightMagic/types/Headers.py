import json

from ._Base import _Base


class Headers(_Base):
    """
        Работа с HTTP заголовками
    """

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        if isinstance(value, dict):
            return value

        elif isinstance(value, str):
            return json.loads(value)

        else:
            raise ValueError

    @staticmethod
    def get_db_type():
        return 'jsonb'
