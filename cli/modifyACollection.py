"""
file: modifyACollection.py
language: python3
author: Dara Prak
description: Functions for adding and deleting a game from a collection, modifying the name of a collection,
            and deleting an entire collection
"""

def addToCollection(curs, username):
    try:
        game = input("Enter the name of the game to add > ")

        # get the id of the game to add
        curs.execute("SELECT gameid FROM games WHERE gametitle = %s", (game,))
        gameid = curs.fetchone()

        # checks if the game exists
        if gameid is None:
            print("Game does not exist")
            return

        collection = input("Enter the name of the collection to add to > ")

        # get the id of the collection to add to
        curs.execute("SELECT collectionid FROM collection WHERE collectionname = %s AND username = %s",
                     (collection, username))
        collectionid = curs.fetchone()

        # checks if the user owns a collection of this name
        if collectionid is None:
            print("Collection does not exist for this user")
            return

        # checks if the game is already in the collection
        curs.execute("SELECT gameid FROM incollection WHERE gameid = %s AND collectionid = %s AND username = %s",
                     (gameid[0], collectionid[0], username))
        checkInCollection = curs.fetchone()
        if checkInCollection is not None:
            print("Game is already in collection")
            return

        # warns the user if they don't own at least one of the platforms that supports the game
        curs.execute("SELECT r.platformid from releasegame r, ownsplatform o "
                     "WHERE r.gameid = %s AND o.username = %s AND r.platformid = o.platformid", (gameid[0], username))
        ownsPlatformOfGame = curs.fetchall()
        if len(ownsPlatformOfGame) == 0:
            print("Warning: User does not own any platform that supports the game")

        # adds the game to the collection
        curs.execute("INSERT INTO incollection(gameid, collectionid, username) VALUES (%s, %s, %s)",
                     (gameid[0], collectionid[0], username))
        curs.execute("COMMIT")
        print("Successfully added " + game + " to " + collection)

    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")

def deleteFromCollection(curs, username):
    try:
        game = input("Enter the name of the game to delete > ")

        # get the id of the game to add
        curs.execute("SELECT gameid FROM games WHERE gametitle = %s", (game,))
        gameid = curs.fetchone()

        # checks if the game exists
        if gameid is None:
            print("Game does not exist")
            return

        collection = input("Enter the name of the collection to delete from > ")

        # get the id of the collection to delete from
        curs.execute("SELECT collectionid FROM collection WHERE collectionname = %s AND username = %s",
                     (collection, username))
        collectionid = curs.fetchone()

        # checks if the user owns a collection of this name
        if collectionid is None:
            print("Collection does not exist for this user")
            return

        # checks if the game is in the collection
        curs.execute("SELECT gameid FROM incollection WHERE gameid = %s AND collectionid = %s AND username = %s",
                     (gameid[0], collectionid[0], username))
        checkInCollection = curs.fetchone()
        if checkInCollection is None:
            print("Game is not in the collection")
            return

        # deletes the game from the collection
        curs.execute("DELETE FROM incollection WHERE gameid = %s AND collectionid = %s AND username = %s",
                     (gameid[0], collectionid[0], username))
        curs.execute("COMMIT")
        print("Successfully deleted " + game + " from " + collection)

    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")

def renameCollection(curs, username):
    try:
        oldName = input("Enter the name of the collection to rename > ")

        # get the id of the collection to rename
        curs.execute("SELECT collectionid FROM collection WHERE collectionname = %s AND username = %s",
                     (oldName, username))
        collectionid = curs.fetchone()

        # checks if the user owns a collection of this name
        if collectionid is None:
            print("Collection does not exist for this user")
            return

        newName = input("Enter new name for the collection > ")

        # renames collection
        curs.execute("UPDATE collection SET collectionname = %s WHERE collectionid = %s and username = %s",
                     (newName, collectionid[0], username))
        curs.execute("COMMIT")
        print("Successfully renamed " + oldName + " to " + newName)

    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")

def deleteCollection(curs, username):
    try:
        collection = input("Enter the name of the collection to delete > ")

        # get the id of the collection to delete
        curs.execute("SELECT collectionid FROM collection WHERE collectionname = %s AND username = %s",
                     (collection, username))
        collectionid = curs.fetchone()

        # checks if the user owns a collection of this name
        if collectionid is None:
            print("Collection does not exist for this user")
            return

        # deletes collection. should cascade for incollection
        curs.execute("DELETE FROM collection WHERE collectionid = %s and username = %s",
                     (collectionid[0], username))
        curs.execute("COMMIT")
        print("Successfully deleted " + collection)

    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
