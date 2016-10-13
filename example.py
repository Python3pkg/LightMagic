import datetime

import LightMagic.types as types
from LightMagic.db.Model import Model


class A(Model):
    _primary_keys = ['id']

    _exclude_from_db_model = [
        'x', 'y', 'z', 'h'
    ]

    int_a = types.Int()
    id = types.Int(allow_none=False)
    float = types.Float()
    byte = types.Byte()
    date = types.Date()

    def test_1(self): ...

    def test_2(self): ...

    def get_fields(self):
        return self.get_model_fields()

    def get_table_name(self):
        return 'table_a'

A.date = dateyнtime.datetime.now().date()
print('A.date', A.date)
# B = A(None)
# C = A(None)
# # print(type(B.int_a))
# print(B.__dict__['int_a'])
# print(type(B.float))
# B.int_a = 5
# C.int_a = 3
#
# C.int_a = None
# print(B.int_a)
# print(C.int_a)
#
# # print(type(B.int))
# # print(type(B.int))
# # print(print(type(B.id)))
# C = A(None)
# D = A(None)
# # print(list(B.get_fields()))
# B.x = 3
# C.x = 5
#
# J = Join(B, fields=B.get_model_fields(), is_debug=True)
# J.join(C, fields=C.get_model_fields(),
#        on=(
#            (
#                (C, 'id'), (B, 'id')
#            ),
#            (
#                (C, 'geo'), (B, 'geo_id')
#            ),
#        )
#    )
# J.join(D, fields=D.get_model_fields(),
#        on=(
#            (
#                (D, 'id'), (B, 'id'),
#                (D, 'geo'), (C, 'id'),
#            ),
#        )
#    )
# J.run()
#
# print(B.x)
# print(C.x)
# print(hash((C, 2, (3,))))
# print(hash((B, 2, (3,))))
