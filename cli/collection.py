"""
file: collection.py
language: python3
author: Dara Prak, Lucie Lim, Colin Gladden
description: All functions relating to collections
"""
# Create a collection
def createCollection(curs, username):
    title = input("Enter the name of the collection: ")
    if title == "":
        print("Please enter a valid collection name")
        return
    try:
        # check if collection name already exists
        curs.execute("SELECT collectionname FROM collection WHERE username = %s AND collectionname = %s", (username, title))
        if curs.fetchone() != None:
            print("You already have a collection with that name")
            return
        # insert collection into collection table
        curs.execute("INSERT INTO collection (username, collectionname) VALUES (%s, %s)", (username, title))
        curs.execute("COMMIT")
        output = "{0} has created a collection named {1}".format(username, title)
        print(output)
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
    return

def renameCollection(curs, username):
    try:
        oldName = input("Enter the name of the collection to rename: ")

        # get the id of the collection to rename
        curs.execute("SELECT collectionid FROM collection WHERE collectionname = %s AND username = %s",
                     (oldName, username))
        collectionid = curs.fetchone()

        # checks if the user owns a collection of this name
        if collectionid is None:
            print("Collection does not exist for this user")
            return

        newName = input("Enter new name for the collection: ")
        if newName == oldName:
            print("New name is the same as the old name")
            return
        elif newName == "":
            print("Collection name cannot be empty")
            return

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
        collection = input("Enter the name of the collection to delete: ")

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

# Displays a list of collections for a user
def viewCollections(curs, username):
    # gets all the collections from a given user in ascending alphabetical order of collection name
    try:
        curs.execute("SELECT collectionid, collectionname FROM collection WHERE username = %s ORDER BY collectionname", (username,))
        collections = curs.fetchall()
        count = len(collections)
        if count == 0:
            print("You have no collections")
            return
        elif count == 1:
            print(f"Showing 1 collection for {username}:")
        else:
            print(f"Showing {count} collections for {username}:")
        # for every collection we show the collection name, num of games in collection, & total time played of the games
        for collection in collections:
            collectionID = collection[0]
            title = collection[1]
            # counts all games for a single collection
            curs.execute("SELECT COUNT(gameid) FROM incollection WHERE collectionid = %s", (collectionID,))
            gameCount = curs.fetchone()
            # gets the total time played in a collection
            curs.execute("SELECT SUM(gs.timeplayed) FROM incollection as inc, gamesession as gs WHERE inc.collectionid = %s AND gs.gameid = inc.gameid", (collectionID,))
            totalPlayedSession = curs.fetchone()
            # prints out the collection info
            print("-"*50)
            print(f"Collection Name: {title}")
            print(f"Total Number of Games: {gameCount[0]}")
            if totalPlayedSession[0] != None:
                print(f"Total Time Played: {totalPlayedSession[0].seconds//3600} hours {(totalPlayedSession[0].seconds//60)%60} minutes")
            else:
                print(f"Total Time Played: 0 hours 0 minutes")
        print("-"*50)

    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")

def addToCollection(curs, username):
    try:
        game = input("Enter the name of the game to add: ")

        # get the id of the game to add
        curs.execute("SELECT gameid FROM games WHERE gametitle = %s", (game,))
        gameid = curs.fetchone()

        # checks if the game exists
        if gameid is None:
            print("Game does not exist")
            return

        collection = input("Enter the name of the collection to add to: ")

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
            print(f"Warning: User does not own any platform which supports the game {game}")
            choice = input("Would you like to add the game anyway? (y/n): ")
            if choice != "y":
                return

        # adds the game to the collection
        curs.execute("INSERT INTO incollection(gameid, collectionid, username) VALUES (%s, %s, %s)",
                     (gameid[0], collectionid[0], username))
        curs.execute("COMMIT")
        print("Successfully added " + game + " to " + collection)

    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")

def removeFromCollection(curs, username):
    try:
        game = input("Enter the name of the game to remove: ")

        # get the id of the game to add
        curs.execute("SELECT gameid FROM games WHERE gametitle = %s", (game,))
        gameid = curs.fetchone()

        # checks if the game exists
        if gameid is None:
            print("Game does not exist")
            return

        collection = input("Enter the name of the collection to remove from: ")

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
        print("Successfully removed " + game + " from " + collection)

    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
