from connector.MySQLConnector import MySQLConnector

if __name__ == '__main__':
    source_con = MySQLConnector('192.168.2.81', '3356', 'root', 'wearelunaon123456')
    dst_con = MySQLConnector()
