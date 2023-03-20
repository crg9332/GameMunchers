"""
file: modifyACollection.py
language: python3
author: Dara Prak
description: Functions for adding and deleting a game from a collection, modifying the name of a collection,
            and deleting an entire collection
"""

def addToCollection(curs, username, args):
    if len(args) != 2:
        print("Usage: addGameToCollection <game> <collection>")
        return
    game = args[0]
    collection = args[1]
    try:
        # get the id of the game to add
        curs.execute("SELECT gameid FROM games WHERE gametitle = %s", (game,))
        gameid = curs.fetchone()

        # checks if the game exists
        if len(gameid) == 0:
            print("Game does not exist")
            return

        # checks if user owns the game by checking all their collections
        curs.execute("SELECT gameid FROM incollection where gameid = %s AND username = %s", (gameid[0], username))
        checkOwnsGame = curs.fetchall()
        if len(checkOwnsGame) == 0:
            print("Game is not owned")
            return

        # get the id of the collection to add to
        curs.execute("SELECT collectionid FROM collection WHERE collectionname = %s AND username = %s",
                     (collection, username))
        collectionid = curs.fetchone()

        # checks if the user owns a collection of this name
        if len(collectionid) == 0:
            print("Collection does not exist for this user")
            return

        # checks if the game is already in the collection
        curs.execute("SELECT gameid FROM incollection WHERE gameid = %s AND collectionid = %s",
                     (gameid[0], collectionid[0]))
        checkInCollection = curs.fetcone()
        if len(checkInCollection) == 1:
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

def deleteFromCollection(curs, username, args):
    pass
def renameCollection(curs, username, args):
    pass
def deleteCollection(curs, username, args):
    pass