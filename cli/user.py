from prettytable import PrettyTable
from prettytable import ALL as ALL

# The application provides an user profile functionality that displays the following information:
# – The number of collections the user has
# – The number of followers
# – The number of following
# – Their top 10 video games (by highest rating, most playtime, or combination)

def profile(curs, username):
    try:
        # Get the number of collections
        curs.execute("SELECT COUNT(*) FROM Collection WHERE username = %s;", (username,))
        numCollections = curs.fetchone()[0]
        # Get the number of followers
        curs.execute("SELECT COUNT(*) FROM Friends WHERE friendee = %s;", (username,))
        numFollowers = curs.fetchone()[0]
        # Get the number of following
        curs.execute("SELECT COUNT(*) FROM Friends WHERE friender = %s;", (username,))
        numFollowing = curs.fetchone()[0]
        # Get the top 10 games by highest rating
        curs.execute("SELECT g.gameTitle, ROUND(AVG(r.starrating), 1)\
                    FROM Games g\
                    LEFT JOIN starrating r ON g.gameID = r.gameID\
                    JOIN incollection c ON g.gameID = c.gameID\
                    WHERE c.username = %s\
                    GROUP BY g.gameTitle\
                    ORDER BY COALESCE(ROUND(AVG(r.starrating), 1), 0) DESC\
                    LIMIT 10;", (username,))
        topRatedGames = curs.fetchall()
        # Get the top 10 games by most playtime
        curs.execute("SELECT g.gameTitle, COALESCE(SUM(p.timeplayed), make_interval(secs => 0))\
                    FROM Games g\
                    LEFT JOIN gamesession p ON g.gameID = p.gameID AND p.username = %s\
                    JOIN incollection c ON g.gameID = c.gameID\
                    WHERE c.username = %s\
                    GROUP BY g.gameTitle\
                    ORDER BY COALESCE(SUM(p.timeplayed), make_interval(secs => 0)) DESC\
                    LIMIT 10;", (username, username))
        topPlayedGames = curs.fetchall()
        # Get the top 10 games by highest rating and most playtime
        curs.execute("SELECT g.gameTitle, ROUND(AVG(r.starrating), 1),\
                     (SELECT COALESCE(SUM(p.timeplayed), make_interval(secs => 0))\
                        FROM gamesession p\
                        WHERE p.gameID = g.gameID AND p.username = %s)\
                    FROM Games g\
                    LEFT JOIN starrating r ON g.gameID = r.gameID\
                    JOIN incollection c ON g.gameID = c.gameID\
                    WHERE c.username = %s\
                    GROUP BY g.gameTitle, g.gameID\
                    ORDER BY COALESCE(ROUND(AVG(r.starrating), 1), 0) DESC, COALESCE((SELECT COALESCE(SUM(p.timeplayed), make_interval(secs => 0))\
                        FROM gamesession p\
                        WHERE p.gameID = g.gameID AND p.username = %s), make_interval(secs => 0)) DESC\
                    LIMIT 10;", (username, username, username))
        topRatedPlayedGames = curs.fetchall()

        # Create table
        table = PrettyTable(hrules=ALL)
        table.field_names = ["Number of Collections", "Number of Followers", "Number of Following"]
        table.add_row([numCollections, numFollowers, numFollowing])
        print(table)
        print()

        print("Top 10 games by highest rating")
        table = PrettyTable(hrules=ALL)
        table.field_names = ["Game Title", "Rating"]
        table.align["Game Title"] = "l"
        table.align["Rating"] = "r"
        for game in topRatedGames:
            if game[1] is None:
                table.add_row([game[0], 'N/A'])
            else:
                table.add_row([game[0], game[1]])
        print(table)
        print()

        print("Top 10 games by most playtime")
        table = PrettyTable(hrules=ALL)
        table.field_names = ["Game Title", "Playtime"]
        table.align["Game Title"] = "l"
        table.align["Playtime"] = "r"
        for game in topPlayedGames:
            # display playtime as hours to the nearest tenth
            # if total playtime is less than 1 hour, display in minutes
            if game[1].total_seconds() < 3600:
                table.add_row([game[0], str(round(game[1].total_seconds() / 60)) + " minutes"])
            else:
                table.add_row([game[0], str(round(game[1].total_seconds() / 3600, 1)) + " hours"])
        print(table)
        print()

        print("Top 10 games by highest rating and most playtime")
        table = PrettyTable(hrules=ALL)
        table.field_names = ["Game Title", "Rating", "Playtime"]
        table.align["Game Title"] = "l"
        table.align["Rating"] = "r"
        table.align["Playtime"] = "r"
        for game in topRatedPlayedGames:
            # display playtime as hours to the nearest tenth
            # if total playtime is less than 1 hour, display in minutes
            if game[2].total_seconds() < 3600:
                # if rating it None, display N/A
                if game[1] is None:
                    table.add_row([game[0], 'N/A', str(round(game[2].total_seconds() / 60)) + " minutes"])
                else:
                    table.add_row([game[0], game[1], str(round(game[2].total_seconds() / 60)) + " minutes"])
            else:
                # if rating it None, display N/A
                if game[1] is None:
                    table.add_row([game[0], 'N/A', str(round(game[2].total_seconds() / 3600, 1)) + " hours"])
                else:
                    table.add_row([game[0], game[1], str(round(game[2].total_seconds() / 3600, 1)) + " hours"])
                    
        print(table)
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
