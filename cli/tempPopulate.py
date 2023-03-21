# RENAME COLLECTIONS WITHOUT SPACES
import psycopg2
from sshtunnel import SSHTunnelForwarder
import os
from dotenv import load_dotenv

load_dotenv()

username_ssh = os.getenv('SSH_USERNAME')
password = os.getenv('PASSWORD')
dbName = os.getenv('DB_NAME')
user_name = None # global variable to store username of logged in user (possibly a temporary solution)

try:
    with SSHTunnelForwarder(
                            ('starbug.cs.rit.edu', 22),
                            ssh_username=username_ssh,
                            ssh_password=password,
                            remote_bind_address=('localhost', 5432)
                            ) as server:
        server.start()
        print("SSH tunnel established")
        params = {
            'database': dbName,
            'user': username_ssh,
            'password': password,
            'host': 'localhost',
            'port': server.local_bind_port
        }
        conn = psycopg2.connect(**params)
        curs = conn.cursor() #comment out after
        print("Database connection established")
        print("Input commands (quit to exit, help for help):")

        curs.execute("SELECT collectionname FROM collection")
        collectionNames = curs.fetchall()
        for collectionName in collectionNames:
            try:
                # curs.execute("UPDATE collection SET collectionname = %s WHERE collectionname = %s",
                #              (collectionName[0].replace(" ", ""), collectionName[0]))
                # curs.execute("COMMIT")
                print(collectionName[0].replace(" ", ""))
            except Exception as e:
                print(e)
                curs.execute("ROLLBACK")
        curs.close()
        conn.close()
        print("Database connection closed")
except Exception as e:
    print(e)
