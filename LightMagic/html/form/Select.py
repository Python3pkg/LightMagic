from .BaseForm import BaseForm


class Select(BaseForm):
    """Отрисовывает форму select"""

    def __init__(self, name, list_of_values=None, allow_empty=False, empty_title=None, value=None, prefix=None,
                 placeholder=None, attributes=None, l_object=None):
        """

        :param name:
        :param list_of_values: list of tupels, or list of values
        :param value:
        :param prefix:
        :param placeholder:
        :param attributes:
        :return:
        """
        if l_object:
            if l_object.__class__.__dict__[name].allow_none:
                list_of_values = ['']
            else:
                list_of_values = []

            list_of_values.extend(l_object.__class__.__dict__[name].list_of_values)

        try:
            self._label = l_object.__class__.__dict__[name].label
        except:
            self._label = None

        super().__init__(name, value=value, prefix=prefix, placeholder=placeholder, attributes=attributes,
                         list_of_values=list_of_values, allow_empty=allow_empty, empty_title=empty_title)

    def render(self):
        """Отрисовывает форму"""

        options = []
        if self._allow_empty is True:
            if self._empty_title is not None:
                title = self._empty_title
            else:
                title = ''
            options.append('<option value="">%s</option>' % title)

        for item in self._list_of_values:
            if isinstance(item, tuple):
                option_value = item[0]
                option_title = item[1]
            else:
                option_value = option_title = str(item)

            if str(option_value) == str(self._value):
                selected = 'selected="selected"'
            else:
                selected = ''

            if self._label:
                option_title = self._label.get(option_value, option_value)
            else:
                option_title = option_value

            options.append('<option value="%s"%s>%s</option>' % (option_value, selected, option_title))

        name = '%s%s' % (self._prefix, self._name)
        return '<select id="%s" name="%s" %s>%s</select>' % (name, name, self._get_attributes(), ' '.join(options))
