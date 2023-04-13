from flask_restx import Resource, Namespace, fields
from models import Game
from connection import DbConnection
from flask import Flask, request, jsonify, make_response

search_ns = Namespace('search', description='Search related operations')

search_title_model = search_ns.model(
    'game',
    {
        'title': fields.String(required=True, description='Game Title'),
    },
)

@search_ns.route('/game')
class SearchGameTitle(Resource):
    @search_ns.expect(search_title_model)
    def post(self):
        data = request.get_json()

        title = data['title']

        # Check for games with similar titles and return them, limit to 10
        conn = DbConnection.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT g.gameTitle, p.platformType, cd.creatorName as developer, cp.creatorName as publisher, \
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
                ORDER BY g.gameTitle, rg.releaseDate;", ("%" + title + "%",))
        results = cur.fetchall()
        conn.commit()
        cur.close()
        DbConnection.close_connection(conn)

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
                    if compiledResultsCount >= 10:
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
        if compiledResultsCount >= 10:
            compiledResults = compiledResults[:10]

        # parse the results so that they can be returned as json
        games = []
        # populate games with serialized results
        for game in compiledResults:
            if game[5] == None:
                game[5] = 'N/A'
            if game[4] != None:
                # if total playtime is less than 1 hour, display in minutes
                if game[4].total_seconds() / 60 < 60:
                    playtime = str(round(game[4].total_seconds() / 60)) + " minutes"
                else:
                    playtime = str(round(game[4].total_seconds() / 60 / 60, 1)) + " hours"
            else:
                playtime = "0 minutes"
            games.append(Game(game[0], game[1], game[2], game[3], playtime, game[5], game[6]).serialize())
        return make_response(jsonify(games), 200)
        # use dumps to return a json string
        # results = games_schema.dump(results)
        # return make_response(jsonify(results), 200)