"""
file: application.py
language: python3
author: Anna Leung, Colin Gladden, Dara Prak, Lucie Lim, Pato Solis
description: Command line application for interacting with the database
"""
import psycopg2
from sshtunnel import SSHTunnelForwarder
import os
from dotenv import load_dotenv
from auth import signup, login

load_dotenv()

username_ssh = os.getenv('SSH_USERNAME')
password = os.getenv('PASSWORD')
dbName = os.getenv('DB_NAME')
user_name = None

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
        # curs = conn.cursor()
        print("Database connection established")
        print("Input commands (quit to exit, help for help):")
        while True:
            command = input("> ")
            if command == 'quit':
                break
            if command == '':
                continue
            if command.startswith('signup'):
                args = command.split(' ')[1:]
                curs = conn.cursor()
                signup(curs, args)
                curs.close()
                continue
            if command.startswith('login'):
                args = command.split(' ')[1:]
                curs = conn.cursor()
                login(curs, args)
                curs.close()
                continue
            # curs.execute(command)
            # print(curs.fetchall())
        curs.close()
        conn.close()
        print("Database connection closed")
except Exception as e:
    print(e)