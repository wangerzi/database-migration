class MigrationOperation:
    migration_database_map = {}
    migration_table_map = {}

    def __init__(self, src_connector, dst_connector):
        self.src_connector = src_connector
        self.dst_connector = dst_connector
        self.dst_connector.start_tran()

    def complete(self):
        self.dst_connector.commit_tran()

    def migration_database_struct(self, database):
        key = "%s.%s.%s" % (self.src_connector, self.dst_connector, database)
        if key in self.migration_database_map:
            return False
        else:
            drop_sql = self.dst_connector.get_drop_database_sql(database)
            create_sql = self.src_connector.get_create_database_sql(database)
            self.dst_connector.execute_sql(drop_sql)
            self.dst_connector.execute_sql(create_sql)
            self.migration_database_map[key] = 1
            return True

    def migration_table_struct(self, database, table):
        key = "%s.%s.%s.%s" % (self.src_connector, self.dst_connector, database, table)
        if key in self.migration_table_map:
            return False
        else:
            drop_sql = self.dst_connector.get_drop_table_sql(database, table)
            create_sql = self.src_connector.get_create_table_sql(database, table)
            self.dst_connector.use_database(database)
            self.dst_connector.execute_sql(drop_sql)
            self.dst_connector.execute_sql(create_sql)
            self.migration_table_map[key] = 1
            return True

    def migration_table_data(self, database, table, rules):
        data = self.src_connector.get_table_data(database, table, rules)
        self.dst_connector.use_database(database)
        num = self.dst_connector.insert_table_data(database, table, data)
        if num is None:
            return -1
        return num
