class A:
    def a(self):
        pass

class B:
    def b(self):
        pass

class UpperAttrMetaclass(type):
    # Метод __new__ вызывается перед __init__
    # Этот метод создаёт обхект и возвращает его,
    # в то время как __init__ просто инициализирует объект, переданный в качестве аргумента.
    # Обычно вы не используете __new__, если только не хотите проконтролировать,
    # как объект создаётся
    # В данном случае созданный объект это класс, и мы хотим его настроить,
    # поэтому мы перегружаем __new__.
    # Можно также сделать что-нибудь в __init__, если хочется.
    # В некоторых более продвинутых случаях также перегружается __call__,
    # но этого мы сейчас не увидим.
    def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)


        print('future_class_name', future_class_name)
        print('future_class_parents', type(future_class_parents), future_class_parents)
        future_class_parents = (B,)

        print('__new__')
        return type(future_class_name, future_class_parents, uppercase_attr)


class MyMeta(type):
    def __new__(meta, name, bases, dct):
        print('-----------------------------------')
        print("Allocating memory for class", name)
        print(meta)
        print(bases)
        print(dct)
        return super(MyMeta, meta).__new__(meta, name, bases, dct)

    def __init__(cls, name, bases, dct):
        print('-----------------------------------')
        print("Initializing class", name)
        print(cls)
        print(bases)
        print(dct)
        super(MyMeta, cls).__init__(name, bases, dct)




class MyTestCase(metaclass=UpperAttrMetaclass):
    def __init__(self):
        print('__init__')


a = MyTestCase()
print('Описание:')
print([x for x in dir(a) if not str(x).startswith('_')])
