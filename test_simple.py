from LightMagic.db.Model import Model
import LightMagic.types as types


class AClass(Model):
    id = types.Int(allow_none=False)
    float = types.Float()
    byte = types.Byte()
    date = types.Date()
    values = types.Enum(list_of_values=['a', 'b', 'c'])

    def get_table_name(self):
        return 'hz.hz'

A = AClass(None)
A.id = 1
A.values = 'e'
