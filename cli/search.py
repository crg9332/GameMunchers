import numpy as np
from datetime import datetime, timedelta, time

def search(curs, args):
    if len(args) != 1:
        print("Usage: search <gameTitle/platform/releaseDate/developers/price/genre>")
    
    #search by gameTitle
    if args[0] == "gameTitle":
        try:
            gameTitle = input("Enter gameTitle")
            curs.execute("SELECT gameid FROM games WHERE gameTitle = %s", (gameTitle))
            gameid = curs.fetchall()
            gameidArray = np.array(gameid)
            for games in gameid:
                findstuff(games)
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            
    #search by platform
    if args[0] == "platform":
        try:
            platform = input("Enter platform")
            curs.execute("SELECT gameid FROM releasegame as r, platforms as p WHERE platformtype = %s AND p.platformid = r.platformid", (platform))
            gameid = curs.fetchall()
            gameidArray = np.array(gameid)
            for games in gameid:
                findstuff(games)
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            
    #search by release date
    if args[0] == "releaseDate":
        try:
            releaseDate = input("Enter release date in the format of year-month-day (xxxx-xx-xx)")
            curs.execute("SELECT gameid FROM releasegame WHERE releasedate = %s", (releaseDate))
            gameid = curs.fetchall()
            gameidArray = np.array(gameid)
            for games in gameid:
                findstuff(games)
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
    
    #search by developers
    if args[0] == "developers":
        try:
            developers = input("Enter developer)")
            curs.execute("SELECT gameid FROM development as d, creator as c WHERE c.creatorname = %s AND d.creatorid = c.creatorid", (developers))
            gameid = curs.fetchall()
            gameidArray = np.array(gameid)
            for games in gameid:
                findstuff(games)
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            
    #search by price
    if args[0] == "price":
        try:
            price = input("Enter price)")
            curs.execute("SELECT gameid FROM releasegame WHERE price = %s", (price))
            gameid = curs.fetchall()
            gameidArray = np.array(gameid)
            for games in gameid:
                findstuff(games)
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            
    #search by genre
    if args[0] == "genre":
        try:
            genre = input("Enter genre)")
            curs.execute("SELECT gameid FROM gamesgenre as a, genre as g WHERE g.genrename = %s AND g.genreid = a.genreid", (genre))
            gameid = curs.fetchall()
            gameidArray = np.array(gameid)
            for games in gameid:
                findstuff(games)
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
               
               
def findstuff(curs, gameid):
    #if game exist
    if len(gameid) == 0:
        print("Game does not exist")
        return
    
    # game name
    curs.execute("SELECT gametitle FROM games WHERE gameid = %s", (gameid))
    gameTitle = curs.fetchone()
    
    # platform
    curs.execute("SELECT platformtype FROM platforms as p, releasegame as r WHERE r.gameid = %s AND r.platformid = p.platformid", (gameid))
    platform = curs.fetchone()
    
    # developer
    curs.execute("SELECT creatorname FROM development as d, creator as c WHERE d.gameid = %s AND c.creatorid = d.creatorid", (gameid))
    developer = curs.fetchall()
    
    # publisher
    curs.execute("SELECT creatorname FROM publishment as p, creator as c WHERE d.gameid = %s AND c.creatorid = p.creatorid", (gameid))
    publisher = curs.fetchone()
    
    # playtime
    curs.execute("SELECT SUM(timeplayed) FROM gamesession WHERE gameid = %s", (gameid))
    playtime = curs.fetchone()
    
    # age and username
    curs.execute("SELECT ratingdate FROM starrating WHERE gameid = %s", (gameid))
    ratingDate = curs.fetchall()
    nowTime = datetime.now()
    age = nowTime - ratingDate
    curs.execute("SELECT username FROM starrating WHERE gameid = %s", (gameid))
    username = curs.fetchall()