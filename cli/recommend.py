from prettytable import PrettyTable
from prettytable import ALL as ALL

def recommend(curs):
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

        ##### top 20 games amongst friends ####
        curs.execute("SELECT g.gametitle, justify_interval(SUM(gs.timeplayed)) AS playedtime FROM friends f \
                      JOIN gamesession gs on f.friender = 'kfennellyes' \
                      JOIN games g on gs.gameid = g.gameid \
                      GROUP BY g.gametitle \
                      ORDER BY playedtime DESC \
                     LIMIT 20;")
        topGamesFriends = curs.fetchall()
        table2 = PrettyTable(hrules = ALL)
        table2.field_names = ["Title"]
        table2.align["Title"] = "l"
        for game in topGamesFriends:
            table2.add_row([game[0]])
        print("\nTop 20 games amongst friends: ")
        print(table2)


    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")

