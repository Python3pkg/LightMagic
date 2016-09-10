from .BaseForm import BaseForm


class TextInput(BaseForm):
    """Отрисовывает text input"""

    def render(self):
        """Отрисовывает форму"""
        name = '%s%s' % (self._prefix, self._name)
        value = 'value="%s"' % self._value if self._value is not None else ''
        return '<input type="text" id="%s" name="%s" %s %s/>' % (name, name, self._get_attributes(), value)
