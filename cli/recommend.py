from prettytable import PrettyTable
from prettytable import ALL as ALL

def recommend(curs, username):
    try:
        ##### top 20 games last 90 days ####
        curs.execute("SELECT gs.gameid, g.gametitle, justify_interval(SUM(gs.timeplayed)) AS playedtime FROM gamesession gs \
                      LEFT JOIN games g on g.gameid = gs.gameid \
                      WHERE startdatetime >= now() - INTERVAL '90 DAY' \
                      GROUP BY gs.gameid, g.gametitle \
                      ORDER BY playedtime DESC \
                      LIMIT 20")
        topGames = curs.fetchall()
        table1 = PrettyTable(hrules=ALL)
        table1.field_names = ["Title"]
        table1.align["Title"] = "l"
        for game in topGames:
            table1.add_row([game[1]])
        print("Top 20 Games in the last 90 days:")
        print(table1)

        #### Top 5 releases of the Month (month and year chosen based on month with highest amount of releases) ####
        curs.execute("SELECT g.gametitle, justify_interval(SUM(gs.timeplayed)) AS playedtime\
                    FROM releasegame rg\
                    JOIN gamesession gs on rg.gameid = gs.gameid\
                    JOIN games g on g.gameid = gs.gameid\
                    WHERE date_trunc('month', rg.releasedate) = '2009-11-01'\
                    GROUP BY g.gametitle\
                    ORDER BY playedtime DESC\
                    LIMIT 5;")
        topFive = curs.fetchall()
        table3 = PrettyTable(hrules = ALL)
        table3.field_names = ["Title"]
        table3.align["Title"] = "l"
        for game in topFive:
            table3.add_row([game[0]])
        print("\nTop 5 games released of the month with most released games:")
        print(table3)

        #### For You Reccommendation based on Genre of games played ####
        if username == None:
            print("\nLogin in for personalized recommendations!")
            return
        
        # Get the most played game
        curs.execute("SELECT gameid, SUM(timeplayed) AS playtime \
                    FROM gamesession \
                    WHERE username = %s \
                    GROUP BY gameid \
                    ORDER BY playtime DESC \
                    LIMIT 1;", (username,))
        topGame = curs.fetchall()

        userGamesSet = None # setting to none before if statement for efficiency when recommending based on friends

        if len(topGame) == 0:
            print("\nPlay games for personalized recommendations to become available")
        else:
            topGameID = topGame[0][0]
            
            # Get the most played games of the genre of user's most played game
            curs.execute("SELECT gs.gameid, g.gametitle, SUM(gs.timeplayed) AS playedtime \
                        FROM gamesession AS gs \
                        INNER JOIN gamesgenre AS gg ON gs.gameid = gg.gameid \
                        INNER JOIN games g on g.gameid = gg.gameid \
                        WHERE gg.genreid = ( \
                        SELECT genreid \
                        FROM gamesgenre \
                        WHERE gameid = %s \
                        ) \
                        GROUP BY gs.gameid, g.gametitle \
                        ORDER BY playedtime DESC", (topGameID,))
            similarGames = curs.fetchall()

            # get a list of all games user has in collections
            curs.execute("SELECT gameid FROM incollection WHERE username = %s", (username,))
            userGames = curs.fetchall()
            userGamesSet = set()
            for game in userGames:
                userGamesSet.add(game[0])

            # Construct table for recommended games based on genre most played by user limit to 20
            table4 = PrettyTable(hrules = ALL)
            table4.field_names = ["Title"]
            table4.align["Title"] = "l"
            numGames = 0
            for game in similarGames:
                if numGames == 20:
                    break
                if game[0] in userGamesSet:
                    continue
                table4.add_row([game[1]])
                numGames += 1
            print("\nTop 20 Games of your most played Genre:")
            print(table4)

        ##### top 20 games amongst friends ####
        curs.execute("SELECT g.gameid, g.gameTitle, justify_interval(SUM(gs.timePlayed)) AS playtime \
                    FROM Games g \
                    JOIN GameSession gs ON g.gameID = gs.gameID \
                    JOIN friends f ON gs.username = f.friendee \
                    WHERE f.friender = %s \
                    GROUP BY g.gameid, g.gameTitle \
                    ORDER BY playtime DESC;", (username,))
        topGamesFriends = curs.fetchall()
        if len(topGamesFriends) == 0:
            # Check if user has friends
            curs.execute("SELECT * FROM friends WHERE friender = %s", (username,))
            friends = curs.fetchall()
            if len(friends) == 0:
                print("\nYou have no friends! Go make some friends!")
            else:
                print("\nYour friends have not played any games!")
            return
        
        if userGamesSet == None: # now you only have to query once if genre recommend works
            # get a list of all games user has in collections
            curs.execute("SELECT gameid FROM incollection WHERE username = %s", (username,))
            userGames = curs.fetchall()
            userGamesSet = set()
            for game in userGames:
                userGamesSet.add(game[0])
        
        table2 = PrettyTable(hrules = ALL)
        table2.field_names = ["Title"]
        table2.align["Title"] = "l"
        numGames = 0
        for game in topGamesFriends:
            if numGames == 20:
                break
            if game[0] in userGamesSet:
                continue
            table2.add_row([game[1]])
            numGames += 1
        print("\nTop 20 unowned games amongst friends: ")
        print(table2)
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")

