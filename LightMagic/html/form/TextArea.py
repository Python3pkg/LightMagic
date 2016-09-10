from .BaseForm import BaseForm


class TextArea(BaseForm):
    """Отрисовывает text area"""

    def render(self):
        """Отрисовывает форму"""
        name = '%s%s' % (self._prefix, self._name)
        return '<textarea id="%s" name="%s" %s>%s</textarea>' % (name, name, self._get_attributes(), self._value if self._value is not None else '')
