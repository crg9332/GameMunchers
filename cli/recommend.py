from prettytable import PrettyTable
from prettytable import ALL as ALL

def recommend(curs):
    try:
        curs.execute("SELECT gs.gameid, g.gametitle, justify_interval(SUM(gs.timeplayed)) AS playedtime FROM gamesession gs \
                      LEFT JOIN games g on g.gameid = gs.gameid \
                      WHERE startdatetime >= now() - INTERVAL '90 DAY' \
                      GROUP BY gs.gameid, g.gametitle \
                      ORDER BY playedtime DESC \
                      LIMIT 20")
        topGames = curs.fetchall()
        table = PrettyTable(hrules=ALL)
        table.field_names = ["Title"]
        table.align["Title"] = "l"
        for game in topGames:
            table.add_row([game[1]])
        print(table)
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")