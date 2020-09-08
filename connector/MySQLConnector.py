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
            rules = {"limit": None, "order": 'asc'}
        cur = self.get_driver().cursor()
        cur.execute("SELECT * FROM %s.%s" % (database, table))

        return cur.fetchall()

    def insert_table_data(self, database, table, data):
        cur = self.get_driver().cursor()
        if not data or len(data) <= 0 or not isinstance(data, list):
            return False
        cols = ','.join(['%s' for _ in range(0, len(data[0]))])
        sql = "INSERT INTO %s.%s VALUES (%s)" % (database, table, cols) # INSERT INTO XX.XX VALUES(%s,%s,%s)
        cur.executemany(sql, data)

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

    def use_database(self, database):
        self.execute_sql('USE %s' % database)

    def execute_sql(self, sql):
        cur = self.get_driver().cursor()
        return cur.execute(sql)

    def start_tran(self):
        self.execute_sql('BEGIN')

    def commit_tran(self):
        self.execute_sql('COMMIT')

    def rollback_tran(self):
        self.execute_sql('ROLLBACK')

