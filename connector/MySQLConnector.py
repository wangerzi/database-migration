from connector.BaseConnector import BaseConnector
import mysql.connector

from exception.ConnectorException import ConnectorException


class MySQLConnector(BaseConnector):

    def __init__(self, host, port, user, passwd):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.driver = None

    def get_driver(self):
        if self.driver is None:
            self.driver = mysql.connector.connect(
                host=self.host,
                user=self.user,
                port=self.port,
                passwd=self.passwd,
            )
        return self.driver

    def get_table_data(self, database, table, rules=None):
        if rules is None:
            rules = {"limit": None}
        cur = self.get_driver().cursor()
        cur.execute("SELECT * FROM %s.%s" % (database, table))

        return cur.fetchall()

    def get_create_table_sql(self, database, table):
        cur = self.get_driver().cursor()
        cur.execute("SHOW CREATE TABLE %s.%s" % (database, table))

        row = cur.fetchone()
        if row:
            return row[1] + ';'
        else:
            raise ConnectorException("Error to get table %s.%s information" % (database, table))

    def get_drop_table_sql(self, database, table):
        return "DROP TABLE IF EXISTS %s.%s;" % (database, table)

