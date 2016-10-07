import uuid

from ._Base import _Base


class UUID4(_Base):
    """
        Работа с UUID
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __get__(self, *args, **kwargs):
        return super().__get__(*args, **kwargs)

    def __set__(self, *args, **kwargs):
        return super().__set__(*args, **kwargs)

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        try:
            if isinstance(value, str):
                return uuid.UUID(value.replace('-', ''), version=4)
            elif isinstance(value, uuid.UUID) or issubclass(value, uuid.UUID):
                if int(value.version) == 4:
                    return value
                else:
                    raise ValueError('Version of UUID is not correct')
            else:
                raise ValueError('Cant check this type')

        except Exception as e:
            raise ValueError('Unknown error: %s' % str(e))

    def get_db_type(self):
        if self.db_type:
            return self.db_type
        return 'uuid'

    @staticmethod
    def db_serialize(value):
        """ Трансформирование объекта в БД. Необходимо для преобразования сложных типов данных. """
        if isinstance(value, uuid.UUID):
            return str(value)
        else:
            return value

    def db_deserialize(self, value):
        try:
            return uuid.UUID(str(value).replace('-', ''), version=4)
        except:
            return value
