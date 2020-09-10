class MigrationOperation:
    migration_database_map = {}
    migration_table_map = {}

    REBUILD_AUTO = 'auto'
    REBUILD_ALWAYS = 'always'
    REBUILD_NEVER = 'never'

    def __init__(self, src_connector, dst_connector):
        self.src_connector = src_connector
        self.dst_connector = dst_connector
        self.dst_connector.start_tran()

    def complete(self):
        self.dst_connector.commit_tran()

    def migration_database_struct(self, database, rebuild=None):
        if rebuild is None:
            rebuild = self.REBUILD_AUTO
        key = "%s.%s.%s" % (self.src_connector, self.dst_connector, database)
        if key in self.migration_database_map:
            return False
        else:
            if rebuild == self.REBUILD_AUTO:
                # compare src create sql with dst create sql
                dst_databases = self.dst_connector.get_databases()
                if database in dst_databases:
                    if self.dst_connector.get_create_database_sql(
                            database) == self.src_connector.get_create_database_sql(database):
                        rebuild = self.REBUILD_NEVER
                    else:
                        rebuild = self.REBUILD_ALWAYS
                else:
                    rebuild = self.REBUILD_ALWAYS
            if rebuild == self.REBUILD_ALWAYS:
                drop_sql = self.dst_connector.get_drop_database_sql(database)
                create_sql = self.src_connector.get_create_database_sql(database)
                self.dst_connector.execute_sql(drop_sql)
                self.dst_connector.execute_sql(create_sql)
                self.migration_database_map[key] = 1
            return True

    def migration_table_struct(self, database, table, rebuild=None):
        if rebuild is None:
            rebuild = self.REBUILD_AUTO
        key = "%s.%s.%s.%s" % (self.src_connector, self.dst_connector, database, table)
        if key in self.migration_table_map:
            return False
        else:
            if rebuild == self.REBUILD_AUTO:
                # compare src create sql with dst create sql
                dst_tables = self.dst_connector.get_database_tables(database)
                if table in dst_tables:
                    if self.dst_connector.get_create_table_sql(
                            database, table) == self.src_connector.get_create_table_sql(database, table):
                        rebuild = self.REBUILD_NEVER
                    else:
                        rebuild = self.REBUILD_ALWAYS
                else:
                    rebuild = self.REBUILD_ALWAYS
            if rebuild == self.REBUILD_ALWAYS:
                drop_sql = self.dst_connector.get_drop_table_sql(database, table)
                create_sql = self.src_connector.get_create_table_sql(database, table)
                self.dst_connector.use_database(database)
                self.dst_connector.execute_sql(drop_sql)
                self.dst_connector.execute_sql(create_sql)
                self.migration_table_map[key] = 1
            return True

    def migration_table_data(self, database, table, rules, rebuild=None):
        if rebuild is None:
            rebuild = self.REBUILD_AUTO

        if rebuild in [self.REBUILD_ALWAYS, self.REBUILD_AUTO]:
            data = self.src_connector.get_table_data(database, table, rules)
            self.dst_connector.use_database(database)
            self.dst_connector.truncate_table(database, table)
            num = self.dst_connector.insert_table_data(database, table, data)
            if num is None:
                return -1
            return num
        return 0
