import re

from ._Base import _Base


class Email(_Base):
    """
        Для работы с email адресами
    """

    # regexp = re.compile(r"""^[-a-z0-9!#$%&'*+/=?^_`{|}~]+(?:\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@[a-z.0-9-]+$""", re.IGNORECASE)

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных
        """
        # if self.regexp.match(value) is None:
        #     raise ValueError('Email-address not valid')
        return str(value)
