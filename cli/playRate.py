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
        curs.execute("SELECT gameid FROM games WHERE gameTitle = %s", game)
        gameid = curs.fetchone()
        # check if game exists
        if len(gameid) == 0:
            print("Game does not exist")
            return
        # get the game id from users collection which checks if they own it
        curs.execute("SELECT gameid FROM inCollection where gameid = %s AND username = %s", gameid[0], username)
        checkOwned = curs.fetchall()
        if len(checkOwned) == 0:
            print("Game is not owned")
            return
        # gets the rating if one already exists, if it doesn't exist it creates an entry else it updates
        curs.execute("SELECT gameid FROM starrating where gameid = %s AND username = %s", gameid[0], username)
        checkReviewed = curs.fetchall()
        if len(checkReviewed) == 0:
            curs.exectue("INSERT INTO StarRating (username, gameID, starRating) VALUES (%s, %s, %s)", username, gameid[0], rate)
            curs.execute("COMMIT")
            print("New rating done!")
            return
        curs.execute("UPDATE starrating SET starrating = %s WHERE gameid = %s AND username = %s", rate, gameid[0], username)
        curs.execute("COMMIT")
        print("Rating updated!")
        return
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")