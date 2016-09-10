import tornado.gen

from ._Model import _Model


class TornadoModel(_Model):
    """ Базовая модель """

    @tornado.gen.coroutine
    def create(self):
        """ Создает объект в БД """
        query, data = self._create()
        cursor = yield self.db.execute(query, data)

        if len(self._get_primary_keys()) > 0:
            result = cursor.fetchall()
            for key in self._get_primary_keys():
                setattr(self, key, self.get_additional_parametr(key, 'db_deserialize')(result[0][key]))

        self._is_created = True

    @tornado.gen.coroutine
    def get_list(self, *args, **kwargs):
        """ Возвращает список записей """
        query, data = self._get_list(*args, **kwargs)
        cursor = yield self.db.execute(query, data)
        return cursor.fetchall()

    @tornado.gen.coroutine
    def load(self, *args, **kwargs):
        """ Загружает информацию о моделе """
        query, data, fields = self._load(*args, **kwargs)

        cursor = yield self.db.execute(query, data)
        result = cursor.fetchone()

        if result is None:
            raise LookupError('Object not found')
        else:
            self.print_debug('-' * 10, 'Загрузка данных в модель', '-' * 10)
            for key in fields:
                try:
                    setattr(self, key, self.get_additional_parametr(key, 'db_deserialize')(result[key]))

                # Игнорируем ошибку присваивания пустого поля (None)
                except ValueError as e:
                    self.print_debug('Ошибка', e)

            self.print_debug('-' * 10, 'Конец загрузки данных в модель', '-' * 10)

            self._is_created = True
            return True

    @tornado.gen.coroutine
    def remove(self):
        """ Удаляем объект"""
        query, data = self._remove()
        yield self.db.execute(query, data)
        self._is_created = False

    @tornado.gen.coroutine
    def update(self):
        """ Обновляем объект """
        query, data = self._update()
        yield self.db.execute(query, data)

    @tornado.gen.coroutine
    def upsert(self):
        """
            Метод обновляет объект, если он существут и создает объект, если он не существуте (не были вызваны)
            методы load/create. Состояние в БД не отслеживается
        """
        if self._is_created:
            yield self.update()
        else:
            yield self.create()
            self._is_created = True
