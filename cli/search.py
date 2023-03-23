from datetime import *

def search(curs):
    userInput = input("Search by (game title, platform, release date, developers, price, genre): ")
    #search by gameTitle
    if userInput == "game title":
        try:
            gameTitle = input("Enter gameTitle: ")
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
                WHERE g.gameTitle ILIKE %s \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, g.ESRB, rg.releaseDate \
                ORDER BY g.gameTitle, rg.releaseDate;", ("%" + gameTitle + "%",))
            
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            
    #search by platform
    if userInput == "platform":
        try:
            platform = input("Enter platform: ")
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
                WHERE p.platformtype = %s \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, g.ESRB, rg.releaseDate \
                ORDER BY g.gameTitle, rg.releaseDate;", (platform,))
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            
    #search by release date
    if userInput == "release date":
        try:
            releaseDate = input("Enter release date in the format of year-month-day (xxxx-xx-xx): ")
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
                WHERE rg.releaseDate = %s \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, g.ESRB, rg.releaseDate \
                ORDER BY g.gameTitle, rg.releaseDate;", (releaseDate,))                
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
    
    #search by developers
    if userInput == "developers":
        try:
            developers = input("Enter developer: ")
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
                WHERE cd.creatorName ILIKE %s \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, g.ESRB, rg.releaseDate \
                ORDER BY g.gameTitle, rg.releaseDate;", ("%" + developers + "%",))                
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            
    #search by price
    if userInput == "price":
        try:
            price = input("Enter price: ")
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
                WHERE rg.price = %s \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, \
                cp.creatorName, g.ESRB, rg.releaseDate \
                ORDER BY g.gameTitle, rg.releaseDate;", (price,))
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")      
    #search by genre
    if userInput == "genre":
        try:
            genre = input("Enter genre: ")
            if (genre) == None:
                print("No results")
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
                WHERE gn.genrename = %s\
                GROUP BY g.gameTitle, p.platformType, cd.creatorName,\
                cp.creatorName, g.ESRB, rg.releaseDate\
                ORDER BY g.gameTitle, rg.releaseDate", (genre,))
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")

    results = curs.fetchall()
    if len(results) == 0:
        print("Cannot search by ", userInput)
        return
    print("|{0: <80}| {1: <10}| {2: <50}| {3: <50}| {4: >20}| {5: >5}|".format("Video Game", "Platform", "Developer", "Publisher", "Playtime", "Average Rating"))
    for result in results:
        result = list(result)
        if result[2] == None:
            result[2] = "None"
        if result[3] == None:
            result[3] = "None"
        if result[4] == None:
            result[4] = "None"
        else:
            result[4] = str(result[4])
        if result[5] == None:
            result[5] = "None"
        print("|{0: <80}| {1: >10}| {2: >50}| {3: >50}| {4: >20}| {5: >14}|".format(result[0], result[1], result[2], result[3], result[4], result[5]))
               
def sort(curs):
    userInput = input("Sort by (video game name, price, genre, and released year): ")
    try:
        if userInput == "video game name":
            curs.execute("SELECT g.gameTitle, rg.price, gn.genrename, DATE_PART('YEAR', rg.releasedate)\
                    FROM Games g JOIN ReleaseGame rg ON rg.gameID = g.gameID\
                    JOIN gamesgenre gg ON g.gameID = gg.gameID\
                    JOIN Genre gn ON gg.genreID = gn.genreID\
                    ORDER BY g.gameTitle\
                    LIMIT 100")
        if userInput == "price":
            curs.execute("SELECT g.gameTitle, rg.price, gn.genrename, DATE_PART('YEAR', rg.releasedate)\
                    FROM Games g JOIN ReleaseGame rg ON rg.gameID = g.gameID\
                    JOIN gamesgenre gg ON g.gameID = gg.gameID\
                    JOIN Genre gn ON gg.genreID = gn.genreID\
                    ORDER BY rg.price\
                    LIMIT 100")
        if userInput == "genre":
            curs.execute("SELECT g.gameTitle, rg.price, gn.genrename, DATE_PART('YEAR', rg.releasedate)\
                    FROM Games g JOIN ReleaseGame rg ON rg.gameID = g.gameID\
                    JOIN gamesgenre gg ON g.gameID = gg.gameID\
                    JOIN Genre gn ON gg.genreID = gn.genreID\
                    ORDER BY gn.genrename\
                    LIMIT 100")
        if userInput == "released year":
            curs.execute("SELECT g.gameTitle, rg.price, gn.genrename, DATE_PART('YEAR', rg.releasedate)\
                    FROM Games g JOIN ReleaseGame rg ON rg.gameID = g.gameID\
                    JOIN gamesgenre gg ON g.gameID = gg.gameID\
                    JOIN Genre gn ON gg.genreID = gn.genreID\
                    ORDER BY rg.releasedate\
                    LIMIT 100")
        results = curs.fetchall()
        if len(results) == 0:
            print("Cannot sort by", userInput)
            return
        print("|{0: <100}| {1: <10}| {2: <20}| {3: <15}|".format("Video Game", "Price", "Genre", "Release Date"))
        for result in results:
            result = list(result)
            if result[2] == None:
                result[2] = "None"
            if result[3] == None:
                result[3] = "None"
            print("|{0: <100}| {1: >10}| {2: >20}| {3: >15}|".format(result[0], result[1], result[2], str(result[3])))
        
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")