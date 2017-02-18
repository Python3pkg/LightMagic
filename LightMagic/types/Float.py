from ._Base import _Base


class Float(_Base):
    """
        Работа с float
    """

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        return float(value)

    def get_db_type(self):
        if self.db_type:
            return self.db_type
        return 'FLOAT'
