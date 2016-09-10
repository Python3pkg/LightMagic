from ._Base import _Base


class CardPan(_Base):
    """
        Работа с Pan карт и проверка корректности pan-а по алогоритму Луна.
    """

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        digits = [int(d) for d in str(value)]
        checksum = sum(digits[-1::-2]) + sum((d * 2 // 10) + (d * 2 % 10) for d in digits[-2::-2])
        if checksum % 10 == 0:
            return value
        raise ValueError