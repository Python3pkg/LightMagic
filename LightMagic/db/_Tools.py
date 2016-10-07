import pprint

import LightMagic.types as types


class _Tools:
    def __hash__(self):
        return id(self)

    def _parse_filter(self, filter_condition, table_alias=None):
        """ Разбираем фильтр """
        data = []
        where = []
        if filter_condition is not None and len(filter_condition) > 0:
            for key in filter_condition:
                if isinstance(filter_condition[key], dict):
                    for operator in filter_condition[key]:
                        value = filter_condition[key][operator]
                        if isinstance(value, (tuple, list)):
                            for val in value:
                                where_item, value = self._parse_filter_item(key, operator, val, table_alias)
                                where.append(where_item)
                                data.append(value)
                        else:
                            where_item, value = self._parse_filter_item(key, operator, value, table_alias)
                            where.append(where_item)
                            data.append(value)

                else:
                    where_item, value = self._parse_filter_item(key, '=', filter_condition[key], table_alias)
                    where.append(where_item)
                    data.append(value)

        return where, data

    def _parse_filter_item(self, key, operator, value, table_alias=None):
        """ Разбирает элемент фильтра """
        # Проверяем входные параметры
        if key not in self.get_model_fields():
            raise ValueError('Некорректный ключ %s в фильтре' % key)

        if operator not in ('=', '<', '>', '>=', '<='):
            raise ValueError('Некорректный оператор %s в фильтре' % operator)

        # Валидация
        type(self).__dict__[key].check_value(self, value)

        # Получение типа данных в БД
        db_type = type(self).__dict__[key].get_db_type()

        # Приводим значение фильтруемого поля в вид, хранимый в БД.
        # Данная подготовка необходима для, например,  для шифрованных полей.
        if isinstance(type(self).__dict__[key], types.CryptoAES):
            value = self._light_magic_values[id(type(self).__dict__[key])]

        where = '{table_alias}{key}{operator}%s{db_type}'.format(
            key=key,
            operator=operator,
            db_type='::%s' % db_type if db_type is not None else '',
            table_alias='%s.' % table_alias if table_alias is not None else ''
        )

        return where, value

    def _debug(self, method, query, data):
        """ Отображение дебага """
        if self.debug_mode:
            print('*' * 100)
            print('Class:', self.__class__, ' | ', 'Method: %s' % method)
            print(query)
            pprint.pprint(data)
            print('*' * 100)

    def print_debug(self, *args, **kwargs):
        """Отображение строки для дебага"""
        if self.debug_mode:
            if args is not None:
                for item in args:
                    print(item, sep=' ')

    @classmethod
    def get_label(cls, key):
        return getattr(cls.__dict__[key], 'label')
