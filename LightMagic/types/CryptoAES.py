from Crypto.Cipher import AES

from ._Base import _Base


class CryptoAES(_Base):
    """
        Работа с шифрованными строками.
        Пробелы в конце строки будут убраны
    """

    def __init__(self, secret_key, initialization_vector, *args, **kwargs):
        # Регулярное выражение
        self._secret_key = secret_key
        self._initialization_vector = initialization_vector
        super().__init__(*args, **kwargs)

    def _validate(self, obj, value):
        """
            Проверяем корректность входных данных.
            Входные данные должны быть строкой
        """
        return str(value)

    def _pack_value(self, value):
        if value is None:
            return None

        # Строка должна быть кратна 16
        # Поэтому недостающие символы добиваем пробелами
        size_in_bytes = len(bytes(value.encode('utf-8')))
        value = '%s%s' % (value, ' ' * (16 - size_in_bytes % 16))
        aes = AES.new(self._secret_key, AES.MODE_CBC, self._initialization_vector)
        return aes.encrypt(value.encode('utf-8'))

    def _unpack_value(self, value):
        if value is None:
            return None

        # Убираем все пробелы справа, которые, возможно, добавили.
        aes = AES.new(self._secret_key, AES.MODE_CBC, self._initialization_vector)
        return aes.decrypt(value).decode('utf-8').rstrip(' ')

    def get_db_type(self):
        return 'bytea'

    def db_serialize(self, value):
        if value is None:
            return None
        return self._pack_value(value)

    def db_deserialize(self, value):
        try:
            if value is None:
                return None
            return self._unpack_value(bytes(value))
        except Exception:
            return bytes(value).decode('utf-8')
