import abc


class BaseConnector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_drop_table_sql(self, table):
        pass

    @abc.abstractmethod
    def get_create_table_sql(self):
        pass

    @abc.abstractmethod
    def get_table_data_sql(self, rules):
        pass
