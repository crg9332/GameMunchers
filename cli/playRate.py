from random import *
from datetime import datetime, timedelta, time

def rate(curs, username, args):
    if len(args) != 2:
        print("Usage: rate <game> <rating>")
        return
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
        if len(gameid) == 0:
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
        if len(checkReviewed) == 0:
            curs.exectue("INSERT INTO StarRating (username, gameID, starRating) VALUES (%s, %s, %s)", (username, gameid[0], rate))
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


# Play random game from collection
def play(curs, username, args):
    if len(args) != 1:
        print("Usage: play <gameTitle/random>")
    if args[0] == "random":
        playRandom(curs, username)
    else:
        playChosen(curs, username, args[0])

    return

def playRandom(curs, username):
    try:
        # Get all games owned by user
        curs.execute("SELECT gameid FROM incollection WHERE username = %s", (username,))
        gamesOwned = curs.fetchall()
        
        # Get a random game id from previous query's results
        random.seed(None)
        randomGame = gamesOwned[random.randint(0, len(gamesOwned))]
        curs.execute("SELECT gameTitle FROM games WHERE gameid = %s", (randomGame[0],))
        gameTitle = curs.fetchall()

        # Prompt user for amount of timeplayed and calculate end dateTime
        timePlayed = input("How long do you want to play {0} for (in minutes)? ".format(gameTitle))
        startDateTime = datetime.now()
        endDateTime = startDateTime + timedelta(minutes=timePlayed)

        # Insert new game session into appropriate table
        curs.execute("INSERT INTO gamesession (username, gameid, startdatetime, enddatetime VALUES (%s, %s, %s, %s)", (username, randomGame[0], startDateTime, endDateTime))
        output = "{0} has been played for {0} minutes!".format(gameTitle, timePlayed)
        print(output)
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
    return

# Play chosen game from collection
def playChosen(curs, username, gameTitle):
    try:
        # Get game id with the provided game title
        curs.execute("SELECT gameid FROM games as g, incollection as in WHERE gameTitle = %s AND g.gameid = in.gameid AND in.username = %s", (gameTitle, username))
        gameId = curs.fetchone()

        # Check if user owns given game
        if len(gameId) == 0:
            print("You do not own {0}".format(gameTitle))
            return
        
        # Prompt user for amount of timeplayed and calculate end dateTime
        timePlayed = input("How long do you want to play {0} for (in minutes)? ".format(gameTitle))
        startDateTime = datetime.now()
        endDateTime = startDateTime + timedelta(minutes=timePlayed)

        # Insert new game session into appropriate table
        curs.execute("INSERT INTO gamesession (username, gameid, startdatetime, enddatetime VALUES (%s, %s, %s, %s)", (username, gameId[0], startDateTime, endDateTime))
        output = "{0} has been played for {0} minutes!".format(gameTitle, timePlayed)
        print(output)
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
    return