from ._Model import _Model


class SynchronousModel(_Model):
    """
        Синхронная модель, работает с синхронным драйвером.
        direvers.SynchronousConnector
    """

    def create(self):
        """ Создает объект в БД """
        query, data = self._create()
        return self.db.query(query, data)

    def get_list(self, *args, **kwargs):
        """ Возвращает список записей """
        query, data = self._get_list(*args, **kwargs)
        query = query.replace('%', '%')
        return self.db.query(query, data)

    def load(self, *args, **kwargs):
        """ Загружает информацию о моделе """
        query, data, fields = self._load(*args, **kwargs)
        cursor = self.db.query(query, data)
        result = cursor.fetchone()

        if result is None:
            raise LookupError('Object not found')
        else:
            self.print_debug('-' * 10, 'Загрузка данных в модель', '-' * 10)
            for key in fields:
                try:
                    setattr(self, key, type(self).__dict__[key].db_deserialize(result[key]))

                # Игнорируем ошибку присваивания пустого поля (None)
                except ValueError as e:
                    self.print_debug('Ошибка', e)

            self.print_debug('-' * 10, 'Конец загрузки данных в модель', '-' * 10)

            self._is_created = True
            return True

    def remove(self):
        """ Удаляем объект"""
        query, data = self._remove()
        return self.db.query(query, data)

    def update(self):
        """ Обновляем объект """
        query, data = self._update()
        return self.db.query(query, data)

    def upsert(self):
        """
            Метод обновляет объект, если он существут и создает объект, если он не существуте (не были вызваны)
            методы load/create. Состояние в БД не отслеживается
        """
        if self._is_created:
            self.update()
        else:
            self.create()
            self._is_created = True
