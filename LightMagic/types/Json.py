import json

from bson import json_util

from ._Base import _Base


class Json(_Base):
    """
        Работа с Json
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
        if self.db_type:
            return self.db_type
        return 'jsonb'

    @staticmethod
    def db_serialize(value):
        """ Трансформирование объекта в БД. Необходимо для преобразования сложных типов данных. """
        if isinstance(value, (dict, list)):
            return json.dumps(value, default=json_util.default)
        else:
            return value
