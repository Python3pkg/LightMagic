import tornado.gen
import momoko


class Model:
    """ Базовая модель """

    # Исключает из модели БД следующие параметры
    _exclude_from_db_model = ['db', 'debug_mode']

    # Список полей, отдаваемый при выводе списка. Опциональный параметр. Если пустой список - возвращает все.
    _list_fields = []

    def __init__(self, db, debug_mode=False):

        # Соединение с БД
        self.db = db

        # В случае True - для данной модели будут печататься запросы в БД и выводиться список аргументов.
        self.debug_mode = debug_mode

        # Сюда загружаем(кэшируем) список полей в модели
        self._model_fields = None

        # Автоматически заполняется при первом запросе
        self._primary_key = []

    def get_table_name(self):
        """ Возвращает имя таблицы. Необходимо переопределить. """
        raise ValueError

    def get_model_fields(self, force_reload=False):
        """ Возвращает поля модели """
        if self._model_fields is None and force_reload is False:
            self._model_fields = tuple(filter(
                lambda x: (x if not str(x).startswith('_') and not callable(
                    getattr(self, x)) and x not in self._exclude_from_db_model else None), dir(self)))

        return self._model_fields

    def get_additional_parametr(self, key, parament):
        """ Возвращает информацию о расширенном параметре """
        return type(self).__dict__[key].__dict__.get(parament, None)

    def _get_primary_keys(self):
        """ Возвращает первичный ключ """
        if len(self._primary_key) == 0:
            for key in self.get_model_fields():
                # Проверяем, что данный ключ является первичным ключем (возможно составным):
                if self.get_additional_parametr(key, 'db_primary_key') is True:
                    self._primary_key.append(key)
        return self._primary_key

    @tornado.gen.coroutine
    def create(self, force_set_primary_key=False):
        """ Создает объект в БД """
        data = []
        values = []
        fields = []
        for key in self.get_model_fields():
            # Проверяем, что данный ключ является первичным ключем (возможно составным):
            # Проверяем ситуацию, что первичный ключ может не иметь автоинримента, а иметь автозначение.
            if key in self._get_primary_keys() and force_set_primary_key is False and self.get_additional_parametr(key,
                                                                                                                   'db_default_value') is None:
                continue

            # Получаем исходное значение
            value = getattr(self, key)
            # Проверяем, что значение None
            if value is None:
                # Если default значение None
                value = self.get_additional_parametr(key, 'db_default_value')
                if value is None:
                    continue

            # Получаем тип в БД
            db_type = type(self).__dict__[key].get_db_type()
            if db_type is None:
                values.append('%s')
            else:
                values.append('%%s::%s' % (db_type))

            # Приводим значение к типу БД
            data.append(type(self).__dict__[key].db_serialize(value))

            # Добавляем наименование поля
            fields.append(key)

        query = 'INSERT INTO {table_name} ({fields}) VALUES({values}) {index_keys}'.format(
            table_name=self.get_table_name(),
            fields=','.join(fields),
            values=','.join(values),
            index_keys=('RETURNING %s' % ','.join(self._get_primary_keys())) if len(
                self._get_primary_keys()) > 0 else ''
        )

        self.db.execute(query, data, callback=(yield tornado.gen.Callback('q1')))

        cursor = yield momoko.WaitOp('q1')
        if len(self._get_primary_keys()) > 0:
            result = cursor.fetchall()
            for key in self._get_primary_keys():
                setattr(self, key, type(self).__dict__[key].db_deserialize(result[0][key]))

    @tornado.gen.coroutine
    def get_list(self, fields=None, limit=100, offset=0, filter_condition=None, order_by=None, order_type='ASC'):
        """ Возвращает список записей """

        if fields is None:
            fields = self.get_model_fields()
        # Делаем хитрый момент, для того, чтобы проверить - корректны ли все запрошенные поля
        else:
            for x in fields:
                if x not in self.get_model_fields():
                    raise ValueError('Неверно заданы поля fields')

        # Формаирует условия
        data = []
        where = []
        if filter_condition is not None and len(filter_condition) > 0:
            for key, operator, value in filter_condition:
                # Проверяем входные параметры
                if key not in self.get_model_fields():
                    raise ValueError('Некорректный ключ %s в фильтре' % key)

                if operator not in ('=', '<', '>', '>=', '<='):
                    raise ValueError('Некорректный оператор %s в фильтре' % operator)

                # Валидация
                type(self).__dict__[key].check_value(self, value)

                # Получение типа данных в БД
                db_type = type(self).__dict__[key].get_db_type()

                where.append('{key}{operator}%s{db_type}'.format(
                    key=key,
                    operator=operator,
                    db_type='::%s' % db_type if db_type is not None else ''
                ))
                data.append(value)

            where = 'WHERE %s' % ' AND '.join(where)
        else:
            where = ''

        # Формируем сортировку
        order_by_str = ''
        if order_by is not None:
            order_by_str = 'ORDER BY {order_by} {order_type}'.format(
                order_by=order_by,
                order_type=order_type
            )
        # Ограничения
        limit_str = ''
        if limit is not None:
            limit_str = 'LIMIT {limit} OFFSET {offset}'.format(
                limit=int(limit),
                offset=int(offset),
            )

        # Формируем запрос
        query = 'SELECT {fields} FROM {table_name} {where} {order_by_str} {limit_str}'.format(
            fields=', '.join(fields),
            table_name=self.get_table_name(),
            order_by_str=order_by_str,
            limit_str=limit_str,
            where=where
        )

        self.db.execute(query, data, callback=(yield tornado.gen.Callback('q1')))
        cursor = yield momoko.WaitOp('q1')
        return cursor.fetchall()

    @tornado.gen.coroutine
    def load(self, fields=None, by_primary_key=True, by_additional_conditions=None):
        """ Загружает информацию о моделе """
        where = []
        data = []
        # Ищем по primary key:
        if by_primary_key is True:
            for key in self._get_primary_keys():
                where.append('%s=%%s' % key)
                data.append(getattr(self, key))
        # Логи
        elif by_additional_conditions is not None:
            for key in by_additional_conditions:
                where.append('%s=%%s' % key)
                data.append(getattr(self, key))
        else:
            raise Exception('Введите условия загрузки объекта')

        if fields is None:
            fields = self.get_model_fields()

        query = 'SELECT {fields} FROM {table_name} WHERE {where}'.format(
            fields=','.join(fields),
            table_name=self.get_table_name(),
            where=' AND '.join(where)
        )

        self.db.execute(query, data, callback=(yield tornado.gen.Callback('q1')))

        cursor = yield momoko.WaitOp('q1')
        result = cursor.fetchall()[0]

        for key in fields:
            try:
                setattr(self, key, setattr(self, key, type(self).__dict__[key].db_deserialize(result[key])))
            # Игнорируем ошибку присваивания пустого поля (None)
            except ValueError:
                pass
        return True

    @tornado.gen.coroutine
    def remove(self):
        """ Удаляем объект"""
        where = []
        data = []
        # Ищем по primary key:
        for key in self._get_primary_keys():
            where.append('%s=%%s' % key)
            data.append(getattr(self, key))
        if len(data) == 0:
            raise PermissionError('Error Primary Key')

        query = """DELETE FROM {table_name} WHERE {primary_key}""".format(
            table_name=self.get_table_name(),
            primary_key=' AND '.join(where)
        )
        self.db.execute(query, data, callback=(yield tornado.gen.Callback('q1')))
        yield momoko.WaitOp('q1')

    @tornado.gen.coroutine
    def update(self):
        """ Обновляем объект """

        # Исключаем первичные ключи из обновления
        updated_fields = list(filter(lambda x: x not in self._get_primary_keys(), self.get_model_fields()))
        data = []
        sub_query = []
        for key in updated_fields:
            db_type = type(self).__dict__[key].get_db_type()
            if db_type is None:
                sub_query.append('{key}=%s'.format(key=key))
            else:
                sub_query.append('{key}=%s::{type}'.format(key=key, type=db_type))

            data.append(type(self).__dict__[key].db_serialize(getattr(self, key)))

        # WHERE
        where = []
        data = []

        # Ищем по primary key:
        for key in self._get_primary_keys():
            where.append('%s=%%s' % key)
            data.append(getattr(self, key))
        if len(data) == 0:
            raise PermissionError('Error Primary Key')

        query = """UPDATE {table_name} SET {fields} WHERE {where}""".format(
            table_name=self.get_table_name(),
            fields=', '.join(sub_query),
            where=' AND '.join(where)
        )

        self.db.execute(query, data, callback=(yield tornado.gen.Callback('q1')))
        yield momoko.WaitOp('q1')

    # def _join_hash_(self):
    #     print({key: getattr(self, key).__repr__() for key in self.get_model_fields()})
    #     return {key: getattr(self, key).__repr__() for key in self.get_model_fields()}

    def __hash__(self):
        return id(self)
