LightMagic
==========
LightMagic is very simple and quick python3 ORM over momoko/psycopg2.

Введение
--------
LightMagic - это простая и быстрая (условно) ORM система для Postgres.

Система позволяет использовать ограниченный набор запросов для конкретной модели, в частности::

* create()
* get_list()
* load()
* remove()
* upsert()

и использовать оператор join() для нескольких моделей.

При необходимости Вы можете легко расширить свою модель дополнительными методами.

LightMagic изначально разрабатывалась как ORM для Tornado +  Postgres, но Вы так же можете использовать одни и те же
модели и для обычных (синхронных) скриптов (например cron).

Простой вариант использования::

    import LightMagic.types as types
    from LightMagic.db.Model import Model
    class ExampleClass(Model):
        """Just Example Class"""
        id = types.Int(value=3, allow_none=False, db_primary_key=True, db_autovalue=True)
        region = types.Str(allow_none=False, db_primary_key=True, db_autovalue=False, db_default_value='Moscow')
        name = types.Str(min_length=3, max_length=10)
        name_2 = types.Str(regexp=re.compile('^[a-z]{1,3}$'))
        cdate = types.DateTime(db_default_value='NOW()')
        udate = types.DateTime(db_default_value='NOW()')
        params = types.Json(db_default_value='{}')
        list = types.List(type_of_elements=int, db_type=None)
        uuid4 = types.UUID4()
        pan = types.CardPan()
        enum = types.Enum(list_of_values=('a', 1, 10, 8))
        lang = types.Language()
        email = types.Email()
        secret_string = types.CryptoAES(secret_key='qnflslglslvn3ogl', initialization_vector='fhwkfnwifh3hfhsh')

        def get_table_name(self):
            return 'test.table'

License
-------
LightMagic is distributed under the MIT license http://www.opensource.org/licenses/mit-license.php
