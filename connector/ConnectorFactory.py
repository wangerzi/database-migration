from connector.MySQLConnector import MySQLConnector
from exception.ConnectorException import ConnectorException


class ConnectorFactory:
    @staticmethod
    def generate(t, args):
        if t == 'mysql':
            return MySQLConnector(**args)
        else:
            raise ConnectorException("Connector type %s is not support" % t)