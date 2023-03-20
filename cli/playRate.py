from random import *
from datetime import datetime, timedelta, time

# rate a game
def rate(curs, username, args):
    if len(args) != 2:
        print("Usage: rate <game> <rating>")
        return
    args[1] = args[1][1:]
    if not args[1].isdigit():
        print("Rating must be a number ")
        return
    game = args[0]
    rate = int(args[1]) # Cast to int in case user typed a floating point
    if rate < 0 or rate > 5:
        print("Rating must be in range 0-5")
        return
    try:
        # get the game id for game they are reviewing
        curs.execute("SELECT gameid FROM games WHERE gameTitle = %s", (game,))
        gameid = curs.fetchone()
        # check if game exists
        if gameid == None:
            print("Game does not exist")
            return
        # get the game id from users collection which checks if they own it
        curs.execute("SELECT gameid FROM inCollection where gameid = %s AND username = %s", (gameid[0], username))
        checkOwned = curs.fetchall()
        if len(checkOwned) == 0:
            print("Game is not owned")
            return
        # gets the rating if one already exists, if it doesn't exist it creates an entry else it updates
        curs.execute("SELECT gameid FROM starrating where gameid = %s AND username = %s", (gameid[0], username))
        checkReviewed = curs.fetchall()
        # curs.execute("COMMIT")
        if len(checkReviewed) == 0:
            curs.execute("INSERT INTO StarRating (username, gameID, starRating) VALUES (%s, %s, %s)", (username, gameid[0], rate))
            curs.execute("COMMIT")
            print("New rating done!")
            return
        curs.execute("UPDATE starrating SET starrating = %s WHERE gameid = %s AND username = %s", (rate, gameid[0], username))
        curs.execute("COMMIT")
        print("Rating updated!")
        return
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")



def playRandom(curs, username):
    try:
        # Get all games owned by user
        curs.execute("SELECT gameid FROM incollection WHERE username = %s", (username,))
        gamesOwned = curs.fetchall()
        
        # Get a random game id from previous query's results
        seed(None)
        randomGame = gamesOwned[randint(0, len(gamesOwned)-1)]
        curs.execute("SELECT gameTitle FROM games WHERE gameid = %s", (randomGame[0],))
        gameTitle = curs.fetchall()

        # Prompt user for amount of timeplayed and calculate end dateTime
        timePlayed = int(input("How long do you want to play {0} for (in minutes)? ".format(gameTitle[0][0])))
        startDateTime = datetime.now()
        endDateTime = startDateTime + timedelta(minutes=timePlayed)

        # Insert new game session into appropriate table
        curs.execute("INSERT INTO gamesession (username, gameid, startdatetime, enddatetime) VALUES (%s, %s, %s, %s)", (username, randomGame[0], startDateTime, endDateTime))
        curs.execute("COMMIT")
        output = "{0} has been played for {1} minutes!".format(gameTitle[0][0], timePlayed)
        print(output)
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
    return

# Play chosen game from collection
def playChosen(curs, username, args):
    if len(args) != 2:
        print("Usage: play <gameTitle>")
        return
    gameTitle = args[0]
    try:
        # Get game id with the provided game title
        curs.execute("SELECT g.gameid FROM games as g, incollection as inc WHERE g.gameTitle = %s AND g.gameid = inc.gameid AND inc.username = %s", (gameTitle, username))
        gameId = curs.fetchone()

        # Check if user owns given game
        if gameId == None:
            print("You do not own {0}".format(gameTitle))
            return
        
        # Prompt user for amount of timeplayed and calculate end dateTime
        timePlayed = int(input("How long do you want to play {0} for (in minutes)? ".format(gameTitle)))
        startDateTime = datetime.now()
        endDateTime = startDateTime + timedelta(minutes=timePlayed)

        # Insert new game session into appropriate table
        curs.execute("INSERT INTO gamesession (username, gameid, startdatetime, enddatetime) VALUES (%s, %s, %s, %s)", (username, gameId[0], startDateTime, endDateTime))
        curs.execute("COMMIT")
        output = "{0} has been played for {1} minutes!".format(gameTitle, timePlayed)
        print(output)
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
    return