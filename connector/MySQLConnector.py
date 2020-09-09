from connector.BaseConnector import BaseConnector
import mysql.connector
import datetime

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

    def get_database_tables(self, database):
        self.use_database(database)
        cur = self.get_driver().cursor()
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()

        return [v[0] for v in tables]

    def get_databases(self):
        cur = self.get_driver().cursor()
        cur.execute("SHOW databases")
        databases = cur.fetchall()

        return [v[0] for v in databases]

    def get_table_data(self, database, table, rules=None):
        default_rules = {"limit": None, "order_field": None, "order": 'asc'}
        if rules is None:
            rules = default_rules
        else:
            rules = {**default_rules, **rules}
        sql = "SELECT * FROM %s.%s" % (database, table)
        if rules["order_field"] and rules["order"]:
            sql = sql + " ORDER BY %s %s" % (rules["order_field"], rules["order"])
        if rules["limit"]:
            sql = sql + " LIMIT %s" % rules["limit"]
        cur = self.get_driver().cursor()
        cur.execute(sql)

        return cur.fetchall()

    def get_table_fields(self, database, table):
        cur = self.get_driver().cursor()
        cur.execute("SHOW COLUMNS FROM %s.%s" % (database, table))
        columns = cur.fetchall()

        return [{"id": v[0], "type": v[1], "null": v[2], "key": v[3], "default": v[4], "extra": v[5]} for v in columns]

    def insert_table_data(self, database, table, data):
        cur = self.get_driver().cursor()
        if not data or len(data) <= 0 or not isinstance(data, list):
            return 0
        # reformat date and datetime, data should be aoa [(1, 2, 3)]
        # for i in range(len(data)):
        #     item = list(data[i])
        #     for j in range(len(item)):
        #         if isinstance(item[j], datetime.datetime):
        #             item[j] = item[j].strftime("%Y-%m-%d %H:%M:%S")
        #         elif isinstance(item[j], datetime.date):
        #             item[j] = item[j].strftime("%Y-%m-%d")
        #     data[i] = tuple(item)
        fields = self.get_table_fields(database, table)
        fields_str = ','.join(['%s' % v["id"] for v in fields])
        cols = ','.join(['%s' for _ in range(0, len(fields))])
        sql = "INSERT INTO %s.%s(%s) VALUES (%s)" % (database, table, fields_str, cols)  # INSERT INTO XX.XX VALUES(%s,%s,%s)
        cur.executemany(sql, data)
        num = cur.rowcount
        # self.get_driver().commit()
        return num

    def get_create_database_sql(self, database):
        cur = self.get_driver().cursor()
        cur.execute("SHOW CREATE DATABASE %s" % database)

        row = cur.fetchone()
        if not row:
            raise ConnectorException("Error to get database %s information" % database)
        return row[1]

    def get_drop_database_sql(self, database):
        return "DROP DATABASE IF EXISTS %s;" % database

    def get_create_table_sql(self, database, table):
        cur = self.get_driver().cursor()
        cur.execute("SHOW CREATE TABLE %s.%s" % (database, table))

        row = cur.fetchone()
        if not row:
            raise ConnectorException("Error to get table %s.%s information" % (database, table))
        return row[1]

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
