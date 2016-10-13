import tornado.gen

from .Model import Model
from ._Tools import _Tools


class JoinBase(_Tools):
    """
        Класс для создания Join связок. Специально не поддерживает более сложные конструкции для быстрой работы.
        Более сложные вещи  пишем ручками.
        *********
        WHERE:
        Формат where = (
            (название поля1, условие сравнения1, значение1),
            (название поля2, условие сравнения2, значение2),
        )

        Пример: (('x', '>', 10), ('x', '<', 20)) раскроется в WHERE x > 10 AND x < 20. Так же проводятся проверки, что
        данный x действительно существтует в модели, приведение типа и защита от sql инъекций.
    """

    _join_types = {
        'inner': 'INNER',
        'left': 'LEFT',
        'right': 'RIGHT',
        'full_outer': 'FULL OUTER',
        'left_outer': 'LEFT OUTER',
        'right_outer': 'RIGHT OUTER',
    }

    def __init__(self, db, model: Model, fields: tuple, filter_condition=None, default_join_type='inner',
                 debug_mode=False,
                 immutable_models=True, order_by=None, order_type='ASC'):
        """

        :param model: Model
        :param fields:
        :param where: tuple
        :param default_join_type:
        :param debug_mode:
        :param immutable_models:
        :return:
        """
        self.db = db

        # Список объектов для join-а
        self._join = []

        # Тип join по-умолчанию.
        self._default_join_type = default_join_type

        # Включен ли debug запроса
        self._debug_mode = debug_mode

        # Объект, с которого начинается join
        self._start_model = model

        # Список полей для отображения в начальном объекте
        self._start_model_fields = fields

        # Условия для начального объекта
        self._start_model_where = filter_condition

        # Тип моделей: изменяемые или не изменяемые. Если структура модели не меняется после первого запуска процесса,
        # тогда оставляйте immutable_models=True. Если модель меняется, тогда требуется immutable_models=False.
        # Это связано с механизмом кэширования хэшей модели для ускорения сборки запроса join.
        self.immutable_models = immutable_models

        # Собранный запрос для данного join
        self._sql_query = None

        self._order_by = order_by
        self._order_type = order_type

    def join(self, model: Model, fields: tuple, on: dict, filter_condition=None, join_type=None):
        """
        Join-ит таблицу.
        :param model:
        :param fields:
        :param on:
        :param filter_condition: tuple
        :param join_type:
        :return:
        """
        if not isinstance(model, Model):
            raise ValueError

        if not isinstance(fields, tuple):
            raise ValueError

        if not isinstance(on, dict):
            raise ValueError

        if not (filter_condition is None or isinstance(filter_condition, tuple)):
            raise ValueError

        join_type = self._default_join_type if join_type is None else join_type
        if join_type not in self._join_types:
            raise ValueError

        join_alias = 't%s' % (len(self._join) + 2)
        self._join.append((model, fields, on, filter_condition, join_type, join_alias))

        return self

    @tornado.gen.coroutine
    def run(self, limit=100, offset=0):
        """ Собирает и выполняет Join """
        # if self._sql_query is None:
        self._sql_query, data = self._compile_query()

        self._sql_query = '%s LIMIT %s OFFSET %s' % (self._sql_query, limit, offset)
        if self._debug_mode:
            print('*' * 30)
            print('SQL QUERY:')
            print(self._sql_query)
            print('data', data)
            print('*' * 30)
        cursor = yield self.db.execute(self._sql_query, data)
        return cursor.fetchall()

    def _compile_query(self) -> str:
        """ Собирает запрос """
        select_fields = self._prepare_fields('t1', self._start_model_fields)
        where, data = self._prepare_where(self._start_model, self._start_model_where, 't1')
        join = []
        join_map = {hash(self._start_model): 't1'}
        for model, fields, on, l_where, join_type, join_alias in self._join:
            join_map[hash(model)] = join_alias
            select_fields.extend(self._prepare_fields(join_alias, fields))

            # Подготавливаем фильтр:
            filter_where, filter_data = self._prepare_where(model, l_where, join_alias)
            where.extend(filter_where)
            data.extend(filter_data)
            # join.append('JOIN %s %s ON %s' % (model.get_table_name(), join_alias, self._prepare_join_on(on)))
            join.append(self._prepare_join(model, join_type, on, join_map))

        query = 'SELECT {fields} FROM {start_table_name} t1 {join} {where} ORDER BY {order_by} {order_type}'.format(
            fields=','.join(select_fields),
            start_table_name=self._start_model.get_table_name(),
            join=' '.join(join),
            where='WHERE %s' % ' AND '.join(where) if len(where) > 0 else '',
            order_by=self._order_by,
            order_type=self._order_type
        )

        return query, data

    @staticmethod
    def _prepare_fields(join_alias, fields):
        if fields is None:
            return []
        else:
            return ['%s.%s' % (join_alias, field) for field in fields]

    def _prepare_join_on(self, on, join_map):
        """ Готовим правило join-а """
        return '='.join(['%s.%s=%s.%s' % (join_map[hash(model)], key,
                                          join_map[hash(on[(model, key)][0])], on[(model, key)][1])
                         for model, key in on])

    def _prepare_join(self, model, join_type, on, join_map):
        if join_type in self._join_types:
            return ' %s JOIN %s %s ON %s' % (self._join_types[join_type], model.get_table_name(), join_map[hash(model)],
                                             self._prepare_join_on(on, join_map))
        else:
            raise ValueError

    @staticmethod
    def _prepare_where(model: Model, filter_condition: tuple, table_alias=None) -> list:
        """ Сборка where """

        return model._parse_filter(filter_condition, table_alias)
        # if filter_condition is None:
        #     return result
        # else:
        #     for key, compare, value in filter_condition:
        #         if compare not in ('>', '>=', '=', '<=', '<'):
        #             raise ValueError('Сompare value not correct')
        #
        #         # Проверяем корректность значения, переданного в filter_condition
        #         # и приводим тип к нужному значению
        #         value = getattr(model, key).check_value(model, value)
        #         result.append('%s %s %s' % (key, compare, value))
        #
        #     return result
