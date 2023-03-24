from prettytable import PrettyTable
from prettytable import ALL as ALL

def addLineBreaks(text, maxLen):
    # if the text is too long, add a line break
    if len(text) > maxLen:
        # find the last space before the max length
        lastSpace = text.rfind(" ", 0, maxLen)
        # if there is no space before the max length, just break at the max length
        if lastSpace == -1:
            lastSpace = maxLen
        # add a line break at the last space
        text = text[:lastSpace] + "\n" + text[lastSpace:]
    return text

def addCommaLineBreaks(text, maxLen):
    # if the text is too long, add a line break
    if len(text) > maxLen:
        # replace all commas with line breaks
        text = text.replace(", ", "\n")
    return text

def search(curs):
    userInput = input("Search by (title, platform, release, developers, price, genre): ")
    searchValue = ""
    
    # search by gameTitle
    if userInput == "title":
        try:
            gameTitle = input("Enter Game Title: ")
            if gameTitle == "":
                print("No results")
                return
            searchValue = gameTitle
            curs.execute("SELECT g.gameTitle, p.platformType, cd.creatorName as developer, cp.creatorName as publisher, \
                (SELECT SUM(gs.timePlayed) FROM GameSession gs WHERE gs.gameID = g.gameID) AS playtime, \
                ROUND(AVG(sr.starRating), 1) AS avgRating, rg.releasedate \
                FROM Games g \
                JOIN ReleaseGame rg ON g.gameID = rg.gameID \
                JOIN Platforms p ON rg.platformID = p.platformID \
                LEFT JOIN Development d ON g.gameID = d.gameID \
                LEFT JOIN Creator cd ON d.creatorID = cd.creatorID \
                LEFT JOIN Publishment pb ON g.gameID = pb.gameID \
                LEFT JOIN Creator cp ON pb.creatorID = cp.creatorID \
                LEFT JOIN StarRating sr ON g.gameID = sr.gameID \
                WHERE g.gameTitle ILIKE %s \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, cp.creatorName, rg.releaseDate, g.gameID \
                ORDER BY g.gameTitle, rg.releaseDate;", ("%" + gameTitle + "%",))
            
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            return
            
    # search by platform
    elif userInput == "platform":
        try:
            # get platform options and display them to user
            curs.execute("SELECT platformType FROM Platforms;")
            platforms = curs.fetchall()
            print("Platform options (case sensitive): ", end = "")
            start = True
            for platform in platforms:
                if start:
                    print(platform[0], end = "")
                    start = False
                else:
                    print(", " + platform[0], end = "")
            print()
            platform = input("Enter Platform: ")
            if platform == "":
                print("No results")
                return
            # check if platform is valid
            curs.execute("SELECT platformType FROM Platforms WHERE platformType = %s;", (platform,))
            if curs.fetchone() == None:
                print(f"Invalid platform \"{platform}\"")
                return
            searchValue = platform
            curs.execute("SELECT g.gameTitle, p.platformType, cd.creatorName as developer, cp.creatorName as publisher, \
                (SELECT SUM(gs.timePlayed) FROM GameSession gs WHERE gs.gameID = g.gameID) AS playtime, \
                ROUND(AVG(sr.starRating), 1) AS avgRating, rg.releasedate \
                FROM Games g \
                JOIN ReleaseGame rg ON g.gameID = rg.gameID \
                JOIN Platforms p ON rg.platformID = p.platformID \
                LEFT JOIN Development d ON g.gameID = d.gameID \
                LEFT JOIN Creator cd ON d.creatorID = cd.creatorID \
                LEFT JOIN Publishment pb ON g.gameID = pb.gameID \
                LEFT JOIN Creator cp ON pb.creatorID = cp.creatorID \
                LEFT JOIN StarRating sr ON g.gameID = sr.gameID \
                WHERE p.platformtype = %s \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, cp.creatorName, rg.releaseDate, g.gameID \
                ORDER BY g.gameTitle, rg.releaseDate;", (platform,))
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            return
            
    # search by release date
    elif userInput == "release":
        try:
            releaseDate = input("Enter release date in the format of year-month-day (xxxx-xx-xx): ")
            if releaseDate == "":
                print("No results")
                return
            searchValue = releaseDate
            curs.execute("SELECT g.gameTitle, p.platformType, cd.creatorName as developer, cp.creatorName as publisher, \
                (SELECT SUM(gs.timePlayed) FROM GameSession gs WHERE gs.gameID = g.gameID) AS playtime, \
                ROUND(AVG(sr.starRating), 1) AS avgRating, rg.releasedate \
                FROM Games g \
                JOIN ReleaseGame rg ON g.gameID = rg.gameID \
                JOIN Platforms p ON rg.platformID = p.platformID \
                LEFT JOIN Development d ON g.gameID = d.gameID \
                LEFT JOIN Creator cd ON d.creatorID = cd.creatorID \
                LEFT JOIN Publishment pb ON g.gameID = pb.gameID \
                LEFT JOIN Creator cp ON pb.creatorID = cp.creatorID \
                LEFT JOIN StarRating sr ON g.gameID = sr.gameID \
                WHERE rg.releaseDate = %s \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, cp.creatorName, rg.releaseDate, g.gameID \
                ORDER BY g.gameTitle, rg.releaseDate;", (releaseDate,))
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            return
    
    # search by developers
    elif userInput == "developers":
        try:
            developers = input("Enter developer: ")
            if developers == "":
                print("No results")
                return
            searchValue = developers
            curs.execute("SELECT g.gameTitle, p.platformType, cd.creatorName as developer, cp.creatorName as publisher, \
                (SELECT SUM(gs.timePlayed) FROM GameSession gs WHERE gs.gameID = g.gameID) AS playtime, \
                ROUND(AVG(sr.starRating), 1) AS avgRating, rg.releasedate \
                FROM Games g \
                JOIN ReleaseGame rg ON g.gameID = rg.gameID \
                JOIN Platforms p ON rg.platformID = p.platformID \
                LEFT JOIN Development d ON g.gameID = d.gameID \
                LEFT JOIN Creator cd ON d.creatorID = cd.creatorID \
                LEFT JOIN Publishment pb ON g.gameID = pb.gameID \
                LEFT JOIN Creator cp ON pb.creatorID = cp.creatorID \
                LEFT JOIN StarRating sr ON g.gameID = sr.gameID \
                WHERE cd.creatorName ILIKE %s \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, cp.creatorName, rg.releaseDate, g.gameID \
                ORDER BY g.gameTitle, rg.releaseDate;", ("%" + developers + "%",))
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            return
            
    # search by price
    elif userInput == "price":
        try:
            print("Prices are in the format of x9.99")
            price = input("Enter price: ")
            if price == "":
                print("No results")
                return
            searchValue = price
            curs.execute("SELECT g.gameTitle, p.platformType, cd.creatorName as developer, cp.creatorName as publisher, \
                (SELECT SUM(gs.timePlayed) FROM GameSession gs WHERE gs.gameID = g.gameID) AS playtime, \
                ROUND(AVG(sr.starRating), 1) AS avgRating, rg.releasedate \
                FROM Games g \
                JOIN ReleaseGame rg ON g.gameID = rg.gameID \
                JOIN Platforms p ON rg.platformID = p.platformID \
                LEFT JOIN Development d ON g.gameID = d.gameID \
                LEFT JOIN Creator cd ON d.creatorID = cd.creatorID \
                LEFT JOIN Publishment pb ON g.gameID = pb.gameID \
                LEFT JOIN Creator cp ON pb.creatorID = cp.creatorID \
                LEFT JOIN StarRating sr ON g.gameID = sr.gameID \
                WHERE rg.price = %s \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, cp.creatorName, rg.releaseDate, g.gameID \
                ORDER BY g.gameTitle, rg.releaseDate;", (price,))
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            return
    
    # search by genre
    elif userInput == "genre":
        try:
            # get the domain of genres for the user to choose from
            curs.execute("SELECT genreName FROM Genre;")
            genreList = curs.fetchall()
            print("Genre options (case sensitive): ", end = "")
            start = True
            for genre in genreList:
                if start:
                    print(genre[0], end = "")
                    start = False
                else:
                    print(", " + genre[0], end = "")
            print()
            genre = input("Enter genre: ")
            if genre == "":
                print("No results")
                return
            # Check if the genre is valid
            curs.execute("SELECT genreName FROM Genre WHERE genreName = %s;", (genre,))
            if curs.fetchone() == None:
                print(f"Invalid genre \"{genre}\"")
                return
            searchValue = genre
            curs.execute("SELECT g.gameTitle, p.platformType, cd.creatorName as developer, cp.creatorName as publisher, \
                (SELECT SUM(gs.timePlayed) FROM GameSession gs WHERE gs.gameID = g.gameID) AS playtime, \
                ROUND(AVG(sr.starRating), 1) AS avgRating, rg.releasedate \
                FROM Games g \
                JOIN ReleaseGame rg ON g.gameID = rg.gameID \
                JOIN Platforms p ON rg.platformID = p.platformID \
                LEFT JOIN Development d ON g.gameID = d.gameID \
                LEFT JOIN Creator cd ON d.creatorID = cd.creatorID \
                LEFT JOIN Publishment pb ON g.gameID = pb.gameID \
                LEFT JOIN Creator cp ON pb.creatorID = cp.creatorID \
                LEFT JOIN StarRating sr ON g.gameID = sr.gameID \
                JOIN gamesgenre gg ON g.gameID = gg.gameID \
                JOIN Genre gn ON gg.genreID = gn.genreID \
                WHERE gn.genrename = %s \
                GROUP BY g.gameTitle, p.platformType, cd.creatorName, cp.creatorName, rg.releaseDate, g.gameID \
                ORDER BY g.gameTitle, rg.releaseDate", (genre,))
        except Exception as e:
            print(e)
            curs.execute("ROLLBACK")
            return
    
    else:
        print(f"Invalid search type \"{userInput}\"")
        return

    results = curs.fetchall()
    if len(results) == 0:
        print(f"No results found for \"{searchValue}\"")
        return
    
    # Bundle duplicate game titles into a single entry with a list of platforms, developers, and publishers
    compiledResults = []
    compiledResultsSet = []
    compiledResultsCount = 0
    for result in results:
        result = list(result)
        if len(compiledResults) == 0:
            compiledResults.append(result[:])
            # format the results to use sets instead of strings
            result[1] = set([result[1]])
            result[2] = set([result[2]])
            result[3] = set([result[3]])
            compiledResultsSet.append(result)
            compiledResultsCount += 1
        else:
            if result[0] == compiledResults[-1][0]:
                if result[1] not in compiledResultsSet[-1][1]:
                    compiledResultsSet[-1][1].add(result[1])
                    compiledResults[-1][1] = compiledResults[-1][1] + ", " + result[1]
                if result[2] != None and result[2] not in compiledResultsSet[-1][2]:
                    compiledResultsSet[-1][2].add(result[2])
                    compiledResults[-1][2] = compiledResults[-1][2] + ", " + result[2]
                if result[3] != None and result[3] not in compiledResultsSet[-1][3]:
                    compiledResultsSet[-1][3].add(result[3])
                    compiledResults[-1][3] = compiledResults[-1][3] + ", " + result[3]
            else:
                if compiledResultsCount >= 100:
                    break
                compiledResults.append(result[:])
                # format the results to use sets instead of strings
                result[1] = set([result[1]])
                result[2] = set([result[2]])
                result[3] = set([result[3]])
                # clear out the old compiledResultsSet to save memory
                compiledResultsSet.clear()
                compiledResultsSet.append(result)
                compiledResultsCount += 1
    
    # cut off the results if there are too many, stop them at 100
    if compiledResultsCount >= 100:
        compiledResults = compiledResults[:100]
        print("Showing top 100 results")
    else:
        print(f"Showing {compiledResultsCount} results")

    # COMMENTED OUT CODE IS FOR PRINTING TABLE WITHOUT prettytable
    # find the length of the longest game title in results
    # maxTitleLength = 5
    # maxPlatformLength = 8
    # maxDeveloperLength = 9
    # maxPublisherLength = 9
    # for result in compiledResults:
    #     if len(result[0]) > maxTitleLength:
    #         maxTitleLength = len(result[0])
    #     if len(result[1]) > maxPlatformLength:
    #         maxPlatformLength = len(result[1])
    #     if result[2] != None and len(result[2]) > maxDeveloperLength:
    #         maxDeveloperLength = len(result[2])
    #     if result[3] != None and len(result[3]) > maxPublisherLength:
    #         maxPublisherLength = len(result[3])
    # maxTitleLength += 2
    # maxPlatformLength += 2
    # maxDeveloperLength += 2
    # maxPublisherLength += 2
    # print("-" * (maxTitleLength + maxPlatformLength + maxDeveloperLength + maxPublisherLength + 20 + 16 + 7))
    # print("|{0:^{1}}|{2:^{3}}|{4:^{5}}|{6:^{7}}|{8:^20}|{9:^16}|".format("Title", maxTitleLength, "Platform", maxPlatformLength, "Developer", maxDeveloperLength, "Publisher", maxPublisherLength, "Playtime", "Average Rating"))
    # for result in compiledResults:
    #     # display playtime as hours to the nearest tenth
    #     if result[4] != None:
    #         playtime = str(round(result[4].total_seconds() / 60 / 60, 1)) + " hours"
    #     else:
    #         playtime = "N/A"
    #     # display results
    #     print("|{0:<{1}}|{2:^{3}}|{4:<{5}}|{6:<{7}}|{8:^20}|{9:^16}|".format(result[0], maxTitleLength, str(result[1]), maxPlatformLength, str(result[2]), maxDeveloperLength, str(result[3]), maxPublisherLength, playtime, str(result[5])))
    # print("-" * (maxTitleLength + maxPlatformLength + maxDeveloperLength + maxPublisherLength + 20 + 16 + 7))
    
    # Print the results in a table using prettytable
    table = PrettyTable(hrules=ALL)
    table.field_names = ["Title", "Platform", "Developer", "Publisher", "Playtime", "Average Rating"]
    table.align["Title"] = "l"
    table.align["Platform"] = "l"
    table.align["Developer"] = "l"
    table.align["Publisher"] = "l"
    table.align["Playtime"] = "r"
    table.align["Average Rating"] = "r"
    for result in compiledResults:
        # display playtime as hours to the nearest tenth
        if result[4] != None:
            # if total playtime is less than 1 hour, display in minutes
            if result[4].total_seconds() / 60 < 60:
                playtime = str(round(result[4].total_seconds() / 60)) + " minutes"
            else:
                playtime = str(round(result[4].total_seconds() / 60 / 60, 1)) + " hours"
        else:
            playtime = "N/A"
        # call functions to perform line breaks
        result[0] = addLineBreaks(result[0], 50)
        result[2] = addCommaLineBreaks(str(result[2]), 30)
        result[3] = addCommaLineBreaks(str(result[3]), 30)

        # display results
        table.add_row([result[0], result[1], result[2], result[3], playtime, result[5]])
    print(table)

def sort(curs):
    sortDomain = set(["title", "price", "genre", "year"])
    userInput = input("Sort by (title, price, genre, year): ")
    while userInput not in sortDomain:
        userInput = input("Invalid input, please try again: ")
    order = input("Ascending or descending (a/d): ")
    while order != "a" and order != "d":
        order = input("Invalid input, please try again: ")
    if order == "a":
        order = "ASC"
    else:
        order = "DESC"
    try:
        if userInput == "title":
            curs.execute("SELECT g.gameTitle, rg.price, ge.genreName, rg.releaseDate\
                    FROM Games g\
                    JOIN ReleaseGame rg ON g.gameID = rg.gameID\
                    JOIN gamesgenre gg ON g.gameID = gg.gameID\
                    JOIN Genre ge ON gg.genreID = ge.genreID\
                    GROUP BY g.gameTitle, rg.price, ge.genreName, rg.releaseDate\
                    ORDER BY g.gameTitle %s\
                    LIMIT 100;" % order)

        elif userInput == "price":
            curs.execute("SELECT g.gameTitle, rg.price, ge.genreName, rg.releaseDate\
                    FROM Games g\
                    JOIN ReleaseGame rg ON g.gameID = rg.gameID\
                    JOIN gamesgenre gg ON g.gameID = gg.gameID\
                    JOIN Genre ge ON gg.genreID = ge.genreID\
                    GROUP BY g.gameTitle, rg.price, ge.genreName, rg.releaseDate\
                    ORDER BY rg.price %s\
                    LIMIT 100;" % order)
        elif userInput == "genre":
            curs.execute("SELECT g.gameTitle, rg.price, ge.genreName, rg.releaseDate\
                    FROM Games g\
                    JOIN ReleaseGame rg ON g.gameID = rg.gameID\
                    JOIN gamesgenre gg ON g.gameID = gg.gameID\
                    JOIN Genre ge ON gg.genreID = ge.genreID\
                    GROUP BY g.gameTitle, rg.price, ge.genreName, rg.releaseDate\
                    ORDER BY ge.genreName %s\
                    LIMIT 100;" % order)
        elif userInput == "year":
            curs.execute("SELECT g.gameTitle, rg.price, ge.genreName, rg.releaseDate\
                    FROM Games g\
                    JOIN ReleaseGame rg ON g.gameID = rg.gameID\
                    JOIN gamesgenre gg ON g.gameID = gg.gameID\
                    JOIN Genre ge ON gg.genreID = ge.genreID\
                    GROUP BY g.gameTitle, rg.price, ge.genreName, rg.releaseDate\
                    ORDER BY rg.releaseDate %s\
                    LIMIT 100" % order)
        else:
            print("Invalid input")
            return
        
        results = curs.fetchall()

        if len(results) == 0:
            print(f"No results found for {userInput}")
            return
        else:
            print(f"Showing top 100 results sorted by {userInput}")
        
        # old display results
        # print("|{0: <100}| {1: <10}| {2: <20}| {3: <15}|".format("Video Game", "Price", "Genre", "Release Date"))
        # for result in results:
        #     result = list(result)
        #     if result[2] == None:
        #         result[2] = "None"
        #     if result[3] == None:
        #         result[3] = "None"
        #     print("|{0: <100}| {1: >10}| {2: >20}| {3: >15}|".format(result[0], result[1], result[2], str(result[3])))
        
        # Display results with prettytable
        table = PrettyTable(hrules=ALL)
        table.field_names = ["Video Game", "Price", "Genre", "Release Year"]
        table.align["Video Game"] = "l"
        table.align["Price"] = "r"
        table.align["Genre"] = "l"
        table.align["Release Year"] = "r"
        for result in results:
            result = list(result)
            table.add_row([result[0], result[1], result[2], str(result[3].year)])
        print(table)
        
    except Exception as e:
        print(e)
        curs.execute("ROLLBACK")
