from . import db_model_class
from .TornadoModel import TornadoModel


class MetaModel(type):
    def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
        future_class_parents = (db_model_class,)
        return type(future_class_name, future_class_parents, {})


class Model(TornadoModel, metaclass=MetaModel):
    """ Базовая модель """
