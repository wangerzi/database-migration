from connector.MySQLConnector import MySQLConnector
from operate.MigrationOperation import MigrationOperation

if __name__ == '__main__':
    con = MySQLConnector('127.0.0.1', '3356', 'root', 'wearelunaon123456')

    print(con.get_table_fields('inssrv', 'sessions'))
    # print(con.get_databases())
    # print(con.get_create_table_sql('inssrv', 'sessions'))
    # print(con.get_drop_table_sql('inssrv', 'sessions'))
    # print(con.get_table_data('inssrv', 'sessions'))

    # try:
    #     con.start_tran()
    #     create_sql = con.get_create_table_sql('inssrv', 'sessions')
    #     drop_sql = con.get_drop_table_sql('inssrv', 'sessions')
    #
    #     data = con.get_table_data('inssrv', 'sessions')
    #
    #     con.use_database('inssrv')
    #     con.execute_sql(drop_sql)  # drop table cannot rollback
    #     con.execute_sql(create_sql)
    #     con.insert_table_data('inssrv', 'sessions', data)
    #     con.commit_tran()
    # except Exception as e:
    #     # con.rollback_tran()
    #     raise e
