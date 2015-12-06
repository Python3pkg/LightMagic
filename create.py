import LightMagic.types as types
from LightMagic.db.Model import Model


class ExampleClass(Model):
    """Просто тестовый класс"""
    id = types.Int(allow_none=False, db_primary_key=True, db_autovalue=True)
    region = types.Str(allow_none=False, db_primary_key=True, db_autovalue=False, db_default_value='Moscow')
    name = types.Str()
    cdate = types.DateTime(db_default_value='NOW()')
    udate = types.DateTime(db_default_value='NOW()')
    params = types.Json(db_default_value='{}')

    def get_table_name(self):
        return 'test.table'


TestObj = ExampleClass(None)
TestObj.id = 1
TestObj.region = 'MSK'
TestObj.name = 'Пользователь'
TestObj.create()
TestObj.remove()
TestObj.get_list(
    fields=['cdate', 'id', 'name', 'params', 'region'],
    limit=1000,
    offset=50,
    filter_condition=[
        ('cdate', '<', '30'),
        ('name', '=', '20'),
        ('params', '=', '{}'),
    ],
    order_by='region',
    order_type='DESC'
)
