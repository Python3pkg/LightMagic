from LightMagic.db._sql_generator import _SqlGenerator
from ._Tools import _Tools


class _Model(_Tools, _SqlGenerator):
    """ Базовая модель """

    # Исключает из модели БД следующие параметры
    _exclude_from_db_model = []

    # Список полей, отдаваемый при выводе списка. Опциональный параметр. Если пустой список - возвращает все.
    _list_fields = []

    _model_fields = None

    def __init__(self, db, debug_mode=False):

        # Соединение с БД
        self.db = db

        # В случае True - для данной модели будут печататься запросы в БД и выводиться список аргументов.
        self.debug_mode = debug_mode

        # Сюда загружаем(кэшируем) список полей в модели
        self._model_fields = None

        # Автоматически заполняется при первом запросе
        self._primary_key = []

        # Добавляем стандартные имена-исключения
        self._exclude_from_db_model.extend(['db', 'debug_mode'])

        # Флаг сохранения в БД. НЕ ПРОВЕРЯЕТСЯ В БД. Меняется на основе методов load/create
        self._is_created = False

    def get_table_name(self):
        """ Возвращает имя таблицы. Необходимо переопределить. """
        raise ValueError

    def get_model_fields(self, force_reload=False):
        """ Возвращает поля модели """
        if self._check_cache('model_fields') is None and force_reload is False:
            model_fields_t = tuple(filter(
                lambda x: (x if not str(x).startswith('_') and not callable(
                    getattr(self, x)) and x not in self._exclude_from_db_model else None), dir(self)))

            model_fields = {key: self.__class__.__dict__[key].__class__ for key in model_fields_t}
            self._set_cache('model_fields', model_fields)

        return self._get_cache('model_fields')

    @classmethod
    def _dig_class(cls, key, oclass):
        if key in oclass.__dict__:
            return oclass.__dict__[key]
        else:
            for p_class in oclass.__bases__:
                if p_class == object:
                    continue
                elif key in p_class.__dict__:
                    return p_class.__dict__[key]
                else:
                    return cls._dig_class(key, p_class)
            raise AttributeError('Key %s not found' % key)

    def get_additional_parametr(self, key, parament):
        """ Возвращает информацию о расширенном параметре """
        # Добавить кэширование
        keyobject = self._dig_class(key, self.__class__)
        return getattr(keyobject, parament)

    def _get_primary_keys(self):
        """ Возвращает первичный ключ """
        if self._check_cache('primary_keys') is None:
            if len(self._primary_key) == 0:
                for key in self.get_model_fields():
                    # Проверяем, что данный ключ является первичным ключем (возможно составным):
                    try:
                        if self.get_additional_parametr(key, 'db_primary_key') is True:
                            self._primary_key.append(key)
                    except:
                        # Первичный ключ не задан
                        pass

            self._set_cache('primary_keys', self._primary_key)
        else:
            self._primary_key = self._get_cache('primary_keys')

        return self._primary_key

    def _create(self):
        """ Создает объект в БД """
        data = []
        values = []
        fields = []
        for key in self.get_model_fields():
            if key in self._get_primary_keys():
                if self.get_additional_parametr(key, 'db_force_set_primary_key') is False:
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
            db_type = self.get_additional_parametr(key, 'get_db_type')()
            if db_type is None:
                values.append('%s')
            else:
                values.append('%%s::%s' % (db_type))

            # Приводим значение к типу БД
            data.append(self.get_additional_parametr(key, 'db_serialize')(value))

            # Добавляем наименование поля
            fields.append(key)

        query = 'INSERT INTO {table_name} ({fields}) VALUES({values}) {index_keys}'.format(
            table_name=self.get_table_name(),
            fields=','.join(fields),
            values=','.join(values),
            index_keys=('RETURNING %s' % ','.join(self._get_primary_keys())) if len(
                self._get_primary_keys()) > 0 else ''
        )

        self._debug('create', query, data)

        return query, data

    def _get_list(self, fields=None, limit=100, offset=0, filter_condition=None, order_by=None, order_type='ASC'):
        """ Возвращает список записей """

        if fields is None:
            fields = self.get_model_fields()
        # Делаем хитрый момент, для того, чтобы проверить - корректны ли все запрошенные поля
        else:
            for x in fields:
                if x not in self.get_model_fields():
                    raise ValueError('Неверно заданы поля fields')

        where, data = self._parse_filter(filter_condition)

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
            where='WHERE %s' % ' AND '.join(where) if len(where) > 0 else ''
        )

        self._debug('get_list', query, data)

        return query, data

    def _load(self, fields=None, by_primary_key=True, filter_condition=None):
        """ Загружает информацию о моделе """
        # Логи
        if filter_condition is not None:
            where, data = self._parse_filter(filter_condition)

        # Ищем по primary key:
        elif by_primary_key is True:
            where = []
            data = []
            for key in self._get_primary_keys():
                where.append('%s=%%s' % key)
                data.append(self.get_additional_parametr(key, 'db_serialize')(getattr(self, key)))
        else:
            raise Exception('Введите условия загрузки объекта')

        if fields is None:
            fields = self.get_model_fields()

        query = 'SELECT {fields} FROM {table_name} WHERE {where}'.format(
            fields=','.join(fields),
            table_name=self.get_table_name(),
            where=' AND '.join(where)
        )
        self._debug('load', query, data)

        return query, data, fields

    def _remove(self):
        """ Удаляем объект"""
        where = []
        data = []
        # Ищем по primary key:
        for key in self._get_primary_keys():
            where.append('%s=%%s' % key)
            data.append(self.get_additional_parametr(key, 'db_serialize')(getattr(self, key)))
        if len(data) == 0:
            raise PermissionError('Error Primary Key')

        query = """DELETE FROM {table_name} WHERE {primary_key}""".format(
            table_name=self.get_table_name(),
            primary_key=' AND '.join(where)
        )

        self._debug('remove', query, data)

        return query, data

    def _update(self):
        """ Обновляем объект """
        keys = []
        if self._check_cache('update_keys') is None:
            # Исключаем первичные ключи из обновления
            updated_fields = list(filter(lambda x: x not in self._get_primary_keys(), self.get_model_fields()))
            # WHERE
            where = []
            sub_query = []

            for key in updated_fields:
                db_type = self.get_additional_parametr(key, 'get_db_type')()
                if db_type is None:
                    sub_query.append('{key}=%s'.format(key=key))
                else:
                    sub_query.append('{key}=%s::{type}'.format(key=key, type=db_type))
                keys.append(key)

            # Ищем по primary key:
            for key in self._get_primary_keys():
                where.append('%s=%%s' % key)
                keys.append(key)

            query = """UPDATE {table_name} SET {fields} WHERE {where}""".format(
                table_name=self.get_table_name(),
                fields=', '.join(sub_query),
                where=' AND '.join(where)
            )
            self._set_cache('update_query', query)
            self._set_cache('update_keys', keys)

        # Заполняем данные
        data = []
        for key in self._get_cache('update_keys'):
            value = getattr(self, key)
            if value is None:
                value = self.get_additional_parametr(key, 'db_default_value')

            data.append(self.get_additional_parametr(key, 'db_serialize')(value))

        # Проверка, что данные действительно загружены и есть ограничения
        if len(data) == 0:
            raise PermissionError('Error Primary Key')

        self._debug('update', self._get_cache('update_query'), data)
        return self._get_cache('update_query'), data

    def _set_cache(self, key, value):
        if self.__class__._compiled_queryies is None:
            self.__class__._compiled_queryies = {}

        self.__class__._compiled_queryies[key] = value

    def _get_cache(self, key):
        if self.__class__._compiled_queryies is None:
            self.__class__._compiled_queryies = {}

        return self.__class__._compiled_queryies[key]

    def _check_cache(self, key):
        if '_compiled_queryies' not in self.__class__.__dict__:
            self.__class__._compiled_queryies = {}

        return self.__class__._compiled_queryies.get(key)
