from sshtunnel import SSHTunnelForwarder
from psycopg2 import pool

# Build a static class to hold the connection pool and tunnel
class DbConnection:
    @staticmethod
    def start(config):
        DbConnection.server = SSHTunnelForwarder(
            ('starbug.cs.rit.edu', 22),
            ssh_username=config.username_ssh,
            ssh_password=config.password,
            remote_bind_address=('localhost', 5432)
        )

        DbConnection.server.start()

        DbConnection.db_pool = pool.SimpleConnectionPool(1, 20,
                                                 user=config.username_ssh,
                                                 password=config.password,
                                                 host='localhost',
                                                 port=DbConnection.server.local_bind_port,
                                                 database=config.database)
        
    @staticmethod
    def get_connection():
        return DbConnection.db_pool.getconn()
    
    @staticmethod
    def close_connection(connection):
        DbConnection.db_pool.putconn(connection)

    @staticmethod
    def close_server():
        DbConnection.server.stop()

# Use the class like this:
# from config import ConnectionConfig
# from connection import DbConnection
#
# config = ConnectionConfig()
# DbConnection.start(config)
# connection = DbConnection.get_connection()
# DbConnection.close_connection(connection)
# DbConnection.close_server()