from LightMagic.db.SynchronousModel import SynchronousModel
import LightMagic.db
LightMagic.db.db_model_class = SynchronousModel

import LightMagic.types as types
from LightMagic.db.Model import Model


class ExampleClass(Model):
    """Просто тестовый класс"""
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

print('Описание:')
print([x for x in dir(ExampleClass) if not str(x).startswith('_')])

TestObj = ExampleClass(None)
print(type(TestObj.list))
TestObj.list.append(6)
print(type(TestObj.list))
# TestObj.id = 1
# TestObj.region = 'MSK'
# TestObj.enum = 'a'
# TestObj.lang = 'ru'
# TestObj.email = 'max--@mxt--c.dmz.dom'
# TestObj.email = 'почта@рф'
# TestObj.secret_string = 'Привет!'
#
# print(TestObj.secret_string)
# # TestObj.name = 'Пользователь'
# # print(TestObj.uuid4)
#
# # TestObj.uuid4 = '0af4964d-3bbc-4fff-bada-236a736b3e1b'
# TestObj.pan = 5469380024038399
# """
# TestObj.create()
# TestObj.remove()
# TestObj.get_list(
#     fields=['cdate', 'id', 'name', 'params', 'region'],
#     limit=1000,
#     offset=50,
#     filter_condition=[
#         ('cdate', '<', '30'),
#         ('name', '=', '20'),
#         ('params', '=', '{}'),
#     ],
#     order_by='region',
#     order_type='DESC'
# )
# """
