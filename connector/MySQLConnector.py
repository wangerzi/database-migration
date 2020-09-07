from connector.BaseConnector import BaseConnector


class MySQLConnector(BaseConnector):
    driver = None

    def __init__(self, host, user, passwd):
        self.host = host
        self.user = user
        self.passwd = passwd

    def get_table_data_sql(self, rules):
        pass

    def get_create_table_sql(self):
        pass

    def get_drop_table_sql(self, table):
        pass
