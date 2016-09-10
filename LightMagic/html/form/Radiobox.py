from .BaseForm import BaseForm


class RadioBox(BaseForm):
    """Отрисовывает radiobox"""

    def render(self):
        """Отрисовывает форму"""
        name = '%s%s' % (self._prefix, self._name)
        value = 'value="%s"' % (self._value if self._value is not None else '1')

        if self._current_status is True:
            checked = 'checked="checked"'
        else:
            checked = ''

        return '<input type="radio" id="%s" name="%s" %s %s %s/>' % (
            name, name, self._get_attributes(), value, checked)
