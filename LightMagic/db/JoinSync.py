from LightMagic.db.JoinBase import JoinBase


class Join(JoinBase):
    """
        Класс для создания Join связок. Специально не поддерживает более сложные конструкции для быстрой работы.
        Более сложные вещи  пишем ручками.
        *********
        WHERE:
        Формат where = (
            (название поля1, условие сравнения1, значение1),
            (название поля2, условие сравнения2, значение2),
        )

        Пример: (('x', '>', 10), ('x', '<', 20)) раскроется в WHERE x > 10 AND x < 20. Так же проводятся проверки, что
        данный x действительно существтует в модели, приведение типа и защита от sql инъекций.
    """

    def run(self, limit=100, offset=0):
        """ Собирает и выполняет Join """
        # if self._sql_query is None:
        self._sql_query, data = self._compile_query()

        self._sql_query = '%s LIMIT %s OFFSET %s' % (self._sql_query, limit, offset)
        if self._debug_mode:
            print('*' * 30)
            print('SQL QUERY:')
            print(self._sql_query)
            print('data', data)
            print('*' * 30)
        self.db.execute(self._sql_query, data)
        return self.db.fetchall()
