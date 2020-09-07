import abc


class BaseConnector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_drop_table_sql(self, database, table):
        pass

    @abc.abstractmethod
    def get_create_table_sql(self, database, table):
        pass

    @abc.abstractmethod
    def get_table_data(self, database, table, rules):
        """
        :param database: mysql database
        :param table: table in database
        :param rules: {"limit": None}
        :return:
        """
        pass
