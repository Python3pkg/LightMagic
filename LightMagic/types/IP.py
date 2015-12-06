import json

from bson import json_util

from ._Base import _Base


class IP(_Base):
    """
        Работа с IP
    """

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        if isinstance(value, dict):
            return value
        elif isinstance(value, list):
            return value
        # Разворачиваем
        elif isinstance(value, str):
            return json.loads(value, object_hook=json_util.object_hook)
        else:
            raise ValueError

    def get_db_type(self):
        return 'inet'
