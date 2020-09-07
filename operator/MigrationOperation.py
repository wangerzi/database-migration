class MigrationOperation:
    def __init__(self, source_connector, dst_connector):
        self.source_connector = source_connector
        self.dst_connector = dst_connector

    def migration_table_struct(self, from_table, dst_table):
        pass

    def migration_table_data(self, from_table, dst_table, args):
        pass
