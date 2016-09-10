import re

import LightMagic.types as types
from LightMagic.db.Model import Model
class ExampleClass(Model):
    """Просто тестовый класс"""
    list = types.List(type_of_elements=int, db_type=None)

TestObj = ExampleClass(None)
TestObj2 = ExampleClass(None)


TestObj.list.append(6)
TestObj2.list.append(3)

print(TestObj.list)
print(TestObj2.list)
