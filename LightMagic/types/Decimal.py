from decimal import Decimal as PythonDecimal

from ._Base import _Base


class Decimal(_Base):
    """
        Работа с int
    """

    def __init__(self, precision=None, scale=None, *args, **kwargs):
        # Точность
        self.precision = precision
        # Масштаб
        self.scale = scale

        super().__init__(*args, **kwargs)

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        return PythonDecimal(value)

    def get_db_type(self):
        """Определяем тип данных"""
        if self.db_type:
            return self.db_type
        if self.precision:
            if self.scale:
                return 'DECIMAL({precision}, {scale})'.format(
                    precision=self.precision,
                    scale=self.scale
                )
            else:
                return 'DECIMAL({precision})'.format(
                    precision=self.precision
                )
        return 'DECIMAL()'
