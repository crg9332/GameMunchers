from flask_marshmallow import Marshmallow

ma = Marshmallow()

class User(ma.Schema):
    class Meta:
        fields = ('username', 'email', 'creationdate', 'lastaccesseddate', 'firstname', 'lastname', 'userpassword')

user_schema = User() # for single user
users_schema = User(many=True) # for multiple users (list)

class User:
    def __init__(self, username, email, creationdate, lastaccesseddate, firstname, lastname, userpassword):
        self.username = username
        self.email = email
        self.creationdate = creationdate
        self.lastaccesseddate = lastaccesseddate
        self.firstname = firstname
        self.lastname = lastname
        self.userpassword = userpassword 

class Game(ma.Schema):
    class Meta:
        fields = ('gametitle', 'platformtype', 'developer', 'publisher', 'playtime', 'avgrating', 'releasedate')

game_schema = Game() # for single game
games_schema = Game(many=True) # for multiple games (list)

class Game:
    def __init__(self, gametitle, platformtype, developer, publisher, playtime, avgrating, releasedate):
        self.gametitle = gametitle
        self.platformtype = platformtype
        self.developer = developer
        self.publisher = publisher
        self.playtime = playtime
        self.avgrating = avgrating
        self.releasedate = releasedate

    # make type game serializable
    def serialize(self):
        # be sure to change any unseralizable types to strings such as DateTimes
        return {
            'gametitle': self.gametitle,
            'platformtype': self.platformtype,
            'developer': self.developer,
            'publisher': self.publisher,
            'playtime': str(self.playtime),
            'avgrating': self.avgrating,
            'releasedate': str(self.releasedate)
        }