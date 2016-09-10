"""
    Класс отвевечает за создание подключения к БД PostgreSQL
    и является менеджером соединений.

    Классы работающие с БД его наследуют
"""
import hashlib
import logging
import random
import re
import time

import psycopg2
import psycopg2.extras

query_replace = re.compile('(%s)')


class SynchronousConnector:
    def __init__(self, config):
        """
            Конструктор парсит настройки БД.
            В качестве метода ожидаем конфиг с настройками
        """
        # Храним настройки соединения с БД
        self._db_config = None

        # Максимальный таймаут перед попытками подключения (сек)
        self._max_timeout = 60

        if self._db_config is None: self._db_config = {}

        self._connection = None

        self._db_config = {
            'host': config['host'],
            'user': config['user'],
            'password': config['password'],
            'port': config['port'],
            'database': config['database'],
        }

    def get_connector(self):
        """
            Метод возвращает дескриптор подключения.
            Коннектор принимает специальный параметр: ctype - тип коннентора.
            Это необходимо, чтобы разделить коннектор для прослушивания "оповещений" и выполнения запросов.
        """

        # Проверяем наличие существующего соединения
        # Если нет - устанавливаем
        # Дескриптора соединения
        if self._connection is None:

            while True:
                # Количество попыток соединения
                number_of_connection_attempts = 0

                try:
                    self._connection = psycopg2.connect(**self._db_config).cursor(
                        cursor_factory=psycopg2.extras.DictCursor)
                    self._connection.connection.set_isolation_level(
                        psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

                    return self._connection

                except Exception as e:
                    logging.warning('Ошибка подключения к СУБД PostgreSQL. Ошибка: %s' % (str(e)))

                # Обрабатываем ошибку подключения
                number_of_connection_attempts += 1

                if number_of_connection_attempts > self._max_timeout:
                    timeout = self._max_timeout
                else:
                    timeout = random.randint(1, number_of_connection_attempts)

                time.sleep(timeout)

        # В случае когда отправлена задача: завершения работы демона - вызываем исключение
        if self._connection is None: raise Exception('Получен сигнал завершения')

        # Десприптор соединяния есть. Проверяем состояние - активно ли соединение
        if self._connection.closed is True:
            # Сбрасываем дескриптор соединения и пытаемся подключиться
            self._connection = None
            return self.get_connector()

        return self._connection

    def query(self, query, data=None):
        """
        Метод осуществляет запрос к БД.
        Запрос надо отправлять через этот метод так как в случае разрыва соединения - пытается поднять соединение
        и отправить запрос еще раз
        """
        self.get_connector().execute(query, data)
        return self.get_connector()
