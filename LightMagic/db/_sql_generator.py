create_table_template = """
CREATE TABLE {tablename}
(
{items},
  CONSTRAINT {pkey_name} PRIMARY KEY ({primary_keys})
)
WITH (
  OIDS = FALSE
)
;


"""


class _SqlGenerator:
    def generate_create_table(self):
        data = []
        for item in self.__class__.__dict__.keys():
            if str(item).startswith('_') or callable(self.__class__.__dict__[item]):
                continue
            field_type = getattr(self.__class__.__dict__[item], 'get_db_type')()
            allow_none = getattr(self.__class__.__dict__[item], 'allow_none')
            db_default_value = getattr(self.__class__.__dict__[item], 'db_default_value')
            data.append('   %s' % '{name} {type} {not_null} {default}'.format(
                name=item,
                type=str(field_type).upper(),
                not_null='NOT NULL' if not allow_none else '',
                default='DEFAULT %s' % db_default_value if db_default_value else ''
            ).strip())
        return create_table_template.format(
            tablename=self.get_table_name(),
            pkey_name=self.get_table_name().replace('.', '_'),
            primary_keys=','.join(self._get_primary_keys()),
            items=',\n'.join(data)
        )
