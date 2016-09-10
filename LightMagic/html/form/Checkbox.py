from .BaseForm import BaseForm


class Checkbox(BaseForm):
    """Отрисовывает checkbox"""

    def __init__(self, name, current_status: bool, **kwargs):
        super().__init__(name, current_status=current_status, **kwargs)

    def render(self):
        """Отрисовывает форму"""
        name = '%s%s' % (self._prefix, self._name)
        value = 'value="%s"' % (self._value if self._value is not None else '1')

        if self._current_status is True:
            checked = 'checked="checked"'
        else:
            checked = ''

        return '<input type="checkbox" id="%s" name="%s" %s %s %s/>' % (
            name, name, self._get_attributes(), value, checked)
