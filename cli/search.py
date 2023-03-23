from datetime import datetime, timedelta, time

def search(curs, args):
    if len(args) != 1:
        print("Usage: search <gameTitle/platform/releaseDate/developers/price/genre>")
    
    #search by gameTitle
    if args[0] == "gameTitle":
        try:
            gameTitle = input("Enter gameTitle")
            if (gameTitle) == None:
                print("No results")
                return
            curs.execute("SELECT g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, SUM(gs.timePlayed) AS playtime, ROUND(AVG(sr.starRating), \
                1) AS avgRating, rg.releasedate FROM Games g JOIN ReleaseGame rg ON \
                g.gameID = rg.gameID JOIN Platforms p ON rg.platformID = p.platformID \
                LEFT JOIN Development d ON g.gameID = d.gameID \
                LEFT JOIN Creator cd ON d.creatorID = cd.creatorID \
                LEFT JOIN Publishment pb ON g.gameID = pb.gameID \
                LEFT JOIN Creator cp ON pb.creatorID = cp.creatorID \
                LEFT JOIN GameSession gs ON g.gameID = gs.gameID \
                LEFT JOIN StarRating sr ON g.gameID = sr.gameID \
                WHERE g.gameTitle ILIKE '%%%s%' \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, g.ESRB, rg.releaseDate \
                ORDER BY g.gameTitle, rg.releaseDate;", (gameTitle))
            results = curs.fetchall()
            
            for result in results:
                print("Video Game Name: %s, Platform: %s, Release Date: %s, \
                    Developer: %s, Publisher %s, Playtime: %s, Average Rating: %s", \
                    (result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
            
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            
    #search by platform
    if args[0] == "platform":
        try:
            platform = input("Enter platform")
            if (platform) == None:
                print("No results")
                return
            curs.execute("SELECT g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, SUM(gs.timePlayed) AS playtime, ROUND(AVG(sr.starRating), \
                1) AS avgRating, rg.releasedate FROM Games g JOIN ReleaseGame rg ON \
                g.gameID = rg.gameID JOIN Platforms p ON rg.platformID = p.platformID \
                LEFT JOIN Development d ON g.gameID = d.gameID \
                LEFT JOIN Creator cd ON d.creatorID = cd.creatorID \
                LEFT JOIN Publishment pb ON g.gameID = pb.gameID \
                LEFT JOIN Creator cp ON pb.creatorID = cp.creatorID \
                LEFT JOIN GameSession gs ON g.gameID = gs.gameID \
                LEFT JOIN StarRating sr ON g.gameID = sr.gameID \
                WHERE p.platformtype = '%s' \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, g.ESRB, rg.releaseDate \
                ORDER BY g.gameTitle, rg.releaseDate;", (platform))
            results = curs.fetchall()
            
            for result in results:
                print("Video Game Name: %s, Platform: %s, Release Date: %s, \
                    Developer: %s, Publisher %s, Playtime: %s, Average Rating: %s", \
                    (result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            
    #search by release date
    if args[0] == "releaseDate":
        try:
            releaseDate = input("Enter release date in the format of year-month-day (xxxx-xx-xx)")
            if (releaseDate) == None:
                print("No results")
                return
            curs.execute("SELECT g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, SUM(gs.timePlayed) AS playtime, ROUND(AVG(sr.starRating), \
                1) AS avgRating, rg.releasedate FROM Games g JOIN ReleaseGame rg ON \
                g.gameID = rg.gameID JOIN Platforms p ON rg.platformID = p.platformID \
                LEFT JOIN Development d ON g.gameID = d.gameID \
                LEFT JOIN Creator cd ON d.creatorID = cd.creatorID \
                LEFT JOIN Publishment pb ON g.gameID = pb.gameID \
                LEFT JOIN Creator cp ON pb.creatorID = cp.creatorID \
                LEFT JOIN GameSession gs ON g.gameID = gs.gameID \
                LEFT JOIN StarRating sr ON g.gameID = sr.gameID \
                WHERE rg.releaseDate = '%s' \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, g.ESRB, rg.releaseDate \
                ORDER BY g.gameTitle, rg.releaseDate;", (releaseDate))
            results = curs.fetchall()
            
            for result in results:
                print("Video Game Name: %s, Platform: %s, Release Date: %s, \
                    Developer: %s, Publisher %s, Playtime: %s, Average Rating: %s", \
                    (result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
                
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
    
    #search by developers
    if args[0] == "developers":
        try:
            developers = input("Enter developer)")
            if (developers) == None:
                print("No results")
                return
            curs.execute("SELECT g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, SUM(gs.timePlayed) AS playtime, ROUND(AVG(sr.starRating), \
                1) AS avgRating, rg.releasedate FROM Games g JOIN ReleaseGame rg ON \
                g.gameID = rg.gameID JOIN Platforms p ON rg.platformID = p.platformID \
                LEFT JOIN Development d ON g.gameID = d.gameID \
                LEFT JOIN Creator cd ON d.creatorID = cd.creatorID \
                LEFT JOIN Publishment pb ON g.gameID = pb.gameID \
                LEFT JOIN Creator cp ON pb.creatorID = cp.creatorID \
                LEFT JOIN GameSession gs ON g.gameID = gs.gameID \
                LEFT JOIN StarRating sr ON g.gameID = sr.gameID \
                WHERE cd.creatorName ILIKE '%%%s%' \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, g.ESRB, rg.releaseDate \
                ORDER BY g.gameTitle, rg.releaseDate;", (developers))
            results = curs.fetchall()
            
            for result in results:
                print("Video Game Name: %s, Platform: %s, Release Date: %s, \
                    Developer: %s, Publisher %s, Playtime: %s, Average Rating: %s", \
                    (result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
                
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            
    #search by price
    if args[0] == "price":
        try:
            price = input("Enter price)")
            if (price) == None:
                print("No results")
                return
            curs.execute("SELECT g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, SUM(gs.timePlayed) AS playtime, ROUND(AVG(sr.starRating), \
                1) AS avgRating, rg.releasedate FROM Games g JOIN ReleaseGame rg ON \
                g.gameID = rg.gameID JOIN Platforms p ON rg.platformID = p.platformID \
                LEFT JOIN Development d ON g.gameID = d.gameID \
                LEFT JOIN Creator cd ON d.creatorID = cd.creatorID \
                LEFT JOIN Publishment pb ON g.gameID = pb.gameID \
                LEFT JOIN Creator cp ON pb.creatorID = cp.creatorID \
                LEFT JOIN GameSession gs ON g.gameID = gs.gameID \
                LEFT JOIN StarRating sr ON g.gameID = sr.gameID \
                WHERE rg.price = '%s' \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, g.ESRB, rg.releaseDate \
                ORDER BY g.gameTitle, rg.releaseDate;", (price))
            results = curs.fetchall()
            
            for result in results:
                print("Video Game Name: %s, Platform: %s, Release Date: %s, \
                    Developer: %s, Publisher %s, Playtime: %s, Average Rating: %s", \
                    (result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
                
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            
    #search by genre
    if args[0] == "genre":
        try:
            genre = input("Enter genre)")
            if (genre) == None:
                print("No results")
                return
            curs.execute("SELECT g.gameTitle, p.platformType, cd.creatorName,\
                cp.creatorName, SUM(gs.timePlayed) AS playtime, ROUND(AVG(sr.starRating),\
                1) AS avgRating, rg.releasedate FROM Games g JOIN ReleaseGame rg ON\
                g.gameID = rg.gameID JOIN Platforms p ON rg.platformID = p.platformID\
                LEFT JOIN Development d ON g.gameID = d.gameID\
                LEFT JOIN Creator cd ON d.creatorID = cd.creatorID\
                LEFT JOIN Publishment pb ON g.gameID = pb.gameID\
                LEFT JOIN Creator cp ON pb.creatorID = cp.creatorID\
                LEFT JOIN GameSession gs ON g.gameID = gs.gameID\
                LEFT JOIN StarRating sr ON g.gameID = sr.gameID\
                JOIN gamesgenre gg ON g.gameID = gg.gameID\
                JOIN Genre gn ON gg.genreID = gn.genreID\
                WHERE gn.genrename = '%s'\
                GROUP BY g.gameTitle, p.platformType, cd.creatorName,\
                cp.creatorName, g.ESRB, rg.releaseDate\
                ORDER BY g.gameTitle, rg.releaseDate", (genre))
            results = curs.fetchall()
            
            for result in results:
                print("Video Game Name: %s, Platform: %s, Release Date: %s, \
                    Developer: %s, Publisher %s, Playtime: %s, Average Rating: %s", \
                    (result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
                
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
               
def sort(curs):
    userInput = input("Sort by (video game name, price, genre, and released year) : ")
    try:
        if userInput.startswith('video'):
            curs.execute("SELECT g.gameTitle, rg.price, gn.genrename, DATE_PART('YEAR', rg.releasedate)\
                    FROM Games g JOIN ReleaseGame rg ON\
                    JOIN gamesgenre gg ON g.gameID = gg.gameID\
                    JOIN Genre gn ON gg.genreID = gn.genreID\
                    ORDER BY g.gameTitle\
                    LIMIT 100")
        if userInput.startswith('price'):
            curs.execute("SELECT g.gameTitle, rg.price, gn.genrename, DATE_PART('YEAR', rg.releasedate)\
                    FROM Games g JOIN ReleaseGame rg ON\
                    JOIN gamesgenre gg ON g.gameID = gg.gameID\
                    JOIN Genre gn ON gg.genreID = gn.genreID\
                    ORDER BY rg.price\
                    LIMIT 100")
        if userInput.startswith('genre'):
            curs.execute("SELECT g.gameTitle, rg.price, gn.genrename, DATE_PART('YEAR', rg.releasedate)\
                    FROM Games g JOIN ReleaseGame rg ON\
                    JOIN gamesgenre gg ON g.gameID = gg.gameID\
                    JOIN Genre gn ON gg.genreID = gn.genreID\
                    ORDER BY gn.genrename\
                    LIMIT 100")
        if userInput.startswith('released'):
            curs.execute("SELECT g.gameTitle, rg.price, gn.genrename, DATE_PART('YEAR', rg.releasedate)\
                    FROM Games g JOIN ReleaseGame rg ON\
                    JOIN gamesgenre gg ON g.gameID = gg.gameID\
                    JOIN Genre gn ON gg.genreID = gn.genreID\
                    ORDER BY rg.releasedate\
                    LIMIT 100")
        else:
            print("%s is an invalid input. Please type video game name, price, genre, or released year.", (input))
            return
        results = curs.fetchall()
            
        for result in results:
            print("Video Game Name: %s, Price: %s, Genre: %s, Release Date: %s", \
                (result[0], result[1], result[2], result[3]))
        
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")