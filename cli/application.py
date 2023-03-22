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
from playRate import rate, playRandom, playChosen
from friends import friend, unfriend
from collection import createCollection, viewCollections
from modifyACollection import *

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
        print("Database connection established")
        print("Input commands (quit to exit, help for help):")
        while True:
            print()
            command = input("> ")
            if command == 'quit':
                break
            elif command == 'help':
                print("Commands:")
                print("signup")
                print("login")
                print("logout")
                print("rate")
                print("play random")
                print("play")
                print("friend")
                print("unfriend")
                print("createCollection")
                print("seeCollection")
                print("quit")
                continue
            elif command == '':
                continue
            elif command.startswith('signup'):
                if user_name != None:
                    print("You are logged in, please log out first.")
                    continue
                curs = conn.cursor()
                signup(curs)
                curs.close()
                continue
            elif command.startswith('login'):
                if user_name != None:
                    print("You are already logged in.")
                    continue
                curs = conn.cursor()
                output = login(curs)
                if output is not None:
                    user_name = output
                curs.close()
                continue
            elif command.startswith('logout'):
                if user_name == None:
                    print("You are not logged in.")
                    continue
                user_name = None
                print("Logged out successfully")
                continue
            elif command.startswith('rate'):
                if user_name == None:
                    print("Please login first.")
                    continue
                curs = conn.cursor()
                rate(curs, user_name)
                curs.close()
                continue
            elif command.startswith('play random'):
                if user_name == None:
                    print("Please login first.")
                    continue
                curs = conn.cursor()
                playRandom(curs, user_name)
                curs.close
                continue
            elif command.startswith('play'):
                if user_name == None:
                    print("Please login first.")
                    continue
                curs = conn.cursor()
                playChosen(curs, user_name)
                curs.close
                continue
            elif command.startswith('friend'):
                if user_name == None:
                    print("Please login first!")
                    continue
                curs = conn.cursor()
                friend(curs, user_name)
                curs.close
                continue
            elif command.startswith('unfriend'):
                if user_name == None:
                    print("Please login first!")
                    continue
                curs = conn.cursor()
                unfriend(curs, user_name)
                curs.close
                continue
            elif command.startswith('createCollection'):
                if user_name == None:
                    print("Please login first.")
                    continue
                curs = conn.cursor()
                createCollection(curs, user_name)
                curs.close()
                continue
            elif command.startswith('viewCollections'):
                if user_name == None:
                    print("Please login first.")
                    continue
                curs = conn.cursor()
                viewCollections(curs, user_name)
                curs.close()
                continue
            if command.startswith('addGameToCollection'):
                args = command.split(' ')[1:]
            if command.startswith('addToCollection'):
                curs = conn.cursor()
                if user_name == None:
                    print("Please login first.")
                    continue
                addToCollection(curs, user_name)
                curs.close()
                continue
            if command.startswith('deleteFromCollection'):
                curs = conn.cursor()
                if user_name == None:
                    print("Please login first.")
                    continue
                deleteFromCollection(curs, user_name)
                curs.close()
                continue
            if command.startswith('renameCollection'):
                curs = conn.cursor()
                if user_name == None:
                    print("Please login first.")
                    continue
                renameCollection(curs, user_name)
                curs.close()
                continue
            if command.startswith('deleteCollection'):
                curs = conn.cursor()
                if user_name == None:
                    print("Please login first.")
                    continue
                deleteCollection(curs, user_name)
                curs.close()
                continue
            # curs.execute(command)
            # print(curs.fetchall())
        # curs.close()
        conn.close()
        print("Database connection closed")
except Exception as e:
    print(e)
