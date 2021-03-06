import abc


class BaseConnector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_database_tables(self, database):
        pass

    @abc.abstractmethod
    def get_databases(self):
        pass

    @abc.abstractmethod
    def get_drop_database_sql(self, database):
        pass

    @abc.abstractmethod
    def get_create_database_sql(self, database):
        pass

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
        :param rules: {"limit": None, "order_field": None, "order": "asc"}
        :return:
        """
        pass

    @abc.abstractmethod
    def get_table_fields(self, database, table):
        pass

    @abc.abstractmethod
    def execute_sql(self, sql):
        """
        execute sql directly
        :param sql:
        :return:
        """
        pass

    @abc.abstractmethod
    def truncate_table(self, database, table):
        pass

    @abc.abstractmethod
    def use_database(self, database):
        pass

    @abc.abstractmethod
    def start_tran(self):
        pass

    @abc.abstractmethod
    def commit_tran(self):
        pass

    @abc.abstractmethod
    def rollback_tran(self):
        pass

    @abc.abstractmethod
    def insert_table_data(self, database, table, data):
        """
        :param database: mysql database
        :param table: table in database
        :param data: [(1, 2, 3), (4, 5, 6)]
        :return:
        """
        pass
