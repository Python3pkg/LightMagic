from ._Base import _Base


class Url(_Base):
    """
        Работа с str
    """

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        if value is None:
            return None
        else:
            return str(value)

    def get_db_type(self):
        if self.db_type:
            return self.db_type
        return 'text'
