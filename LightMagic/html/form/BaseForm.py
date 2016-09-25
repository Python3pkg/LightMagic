from tornado.web import escape


class BaseForm:
    """Базовый класс для форм"""

    def __init__(self, name, value=None, prefix=None, placeholder=None, attributes=None, is_escape=True, process=None, **kwargs):
        """Конструктор"""
        self._name = name
        self._value = value
        self._prefix = '' if prefix is None else prefix
        self._placeholder = placeholder
        self._attributes = attributes
        self._process = process

        if is_escape:
            if isinstance(value, list):
                self._value = [escape.xhtml_escape(x) for x in self._value]
            elif isinstance(value, tuple):
                self._value = tuple([escape.xhtml_escape(x) for x in self._value])
            elif isinstance(value, str):
                self._value = escape.xhtml_escape(self._value)

        # Устанавливаем дополнительные аттрибуты
        for item in kwargs:
            setattr(self, '_%s' % item, kwargs[item])

        if self._process and self._value:
            self._value = self._process(self._value)

            # # Забрать из настроек
            # self._default_value = self._cls.__dict__[self._key].value

    def render(self):
        """Отрисовывает форму"""
        raise PermissionError('Данный метод необходимо переопределить')

    def _get_attributes(self):
        """Возвращает дополнительные аргументы (настройки стиля и т.д.)"""
        if self._attributes is None:
            return ''

        attributes = []
        for key in self._attributes:
            attributes.append('%s="%s"' % (key, self._attributes[key]))

        return ' '.join(attributes)
