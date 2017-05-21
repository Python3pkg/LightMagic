import collections
# Шаблон первичного ключа
primary_key_template = """,CONSTRAINT {pkey_name} PRIMARY KEY ({primary_keys})"""

# Шаблон удаления таблицы
drop_table_template = """DROP TABLE IF EXISTS {table_name} CASCADE;"""

# Шаблон комментария к колонке
comment_template = """COMMENT ON COLUMN {table_name}.{field} IS '{comment}';"""

# Шаблон общего создания таблицы
create_table_template = """\
{drop_table}
CREATE TABLE {table_name}
(
{items}
{primary_key}
)
WITH (
  OIDS = FALSE
);
{comments}
"""


class _SqlGenerator:
    def generate_create_table(self, with_drop=False):
        if with_drop:
            drop_table = drop_table_template.format(table_name=self.get_table_name())
        else:
            drop_table = ''

        data = []
        comments = []
        for item in sorted(self.__class__.__dict__.keys()):
            if str(item).startswith('_') or isinstance(self.__class__.__dict__[item], collections.Callable):
                continue
            field_type = getattr(self.__class__.__dict__[item], 'get_db_type')()
            if getattr(self.__class__.__dict__[item], 'db_autovalue') is True:
                if str(field_type).upper() == 'BIGINT':
                    field_type = 'BIGSERIAL'

            allow_none = getattr(self.__class__.__dict__[item], 'allow_none')
            db_default_value = getattr(self.__class__.__dict__[item], 'db_default_value')
            data.append('   %s' % '{name} {type} {not_null} {default}'.format(
                name=item,
                type=str(field_type).upper(),
                not_null='NOT NULL' if not allow_none else '',
                default='DEFAULT %s' % db_default_value if db_default_value else ''
            ).strip())

            label = getattr(self.__class__.__dict__[item], 'label')
            if label:
                comments.append(comment_template.format(
                    table_name=self.get_table_name(),
                    comment=label.replace("'", "\'"),
                    field=item
                ))

        # Генерируем первичный ключ
        if len(self._get_primary_keys()) > 0:
            primary_key = primary_key_template.format(
                primary_keys=','.join(self._get_primary_keys()),
                pkey_name=self.get_table_name().replace('.', '_'),
            )
        else:
            primary_key = ''

        # Возвращаем шаблон
        return create_table_template.format(
            drop_table=drop_table,
            table_name=self.get_table_name(),
            pkey_name=self.get_table_name().replace('.', '_'),
            primary_key=primary_key,
            items=',\n'.join(data),
            comments='\n'.join(comments)
        )
