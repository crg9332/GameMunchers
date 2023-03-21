from random import *

# Create a collection
# args is the collection name
def createCollection(curs, username, args):
    if len(args) != 1:
        print("Usage: createCollection <title>")
        return    
    title = args[0]
    try:
        curs.execute("INSERT INTO collection (username, collectionname) VALUES (%s, %s)", (username, title))
        curs.execute("COMMIT")
        output = "{0} has created a collection name {1}".format(username, title)
        print(output)
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
    return

# Sees list of collections for a user
def seeCollection(curs, username):
    #gets all the collections from a given user in ascending order
    try:
        curs.execute("SELECT collectionid, collectionname FROM collection WHERE username = %s ORDER BY collectionname", (username,))
        collections = curs.fetchall()
        if len(collections) == 0:
            print("You have no collections")
            return
        #for every collection we show the collection name, num of games in collection, & total time played of the games
        for collection in collections:
            collectionID = collection[0]
            title = collection[1]
            # counts all games for a single collection
            curs.execute("SELECT COUNT(gameid) FROM incollection WHERE collectionid = %s", (collectionID,))
            gameCount = curs.fetchone()
            # gets the total time played in a collection
            curs.execute("SELECT SUM(gs.timeplayed) FROM incollection as inc, gamesession as gs WHERE inc.collectionid = %s AND gs.gameid = inc.gameid", (collectionID,))
            totalPlayedSession = curs.fetchone()
            
            output = "Username: {0} \nCollection Name: {1} \nTotal Number of Games: {2} \nTotal Time Played: {3}\n".format(username, title, gameCount[0], str(totalPlayedSession[0]))
            print(output)

    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
