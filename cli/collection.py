# Create a collection
def createCollection(curs, username):
    title = input("Enter the name of the collection: ")
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
