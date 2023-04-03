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
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")

