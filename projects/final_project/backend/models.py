from config import db


class Player(db.Model):

    __bind_key__ = None
    __tablename__ = "player"

    """Player class"""
    """
    GP: games played
    GS: games started
    MIN: minutes played
    G: goals
    A: assists
    PTS: points (Might need to change this point system they use)
    PTS_G: points per game
    SH: shots
    SH_G: avg shots per game
    SOG: shots on goal
    YC: yellow cards
    RC: Red cards
    GW: games winning
    PK_ATT : penaltyGoals-penaltyShotsAttempted
    CP : Current price
    price: price to buy the player
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    college = db.Column(db.String)
    year = db.Column(db.Integer)

    GP = db.Column(db.Integer)
    GS = db.Column(db.Integer)
    MIN = db.Column(db.Integer)
    G = db.Column(db.Integer)
    A = db.Column(db.Integer)
    PTS = db.Column(db.Integer)
    PTS_G = db.Column(db.Float)
    SH = db.Column(db.Integer)
    SH_G = db.Column(db.Float)
    SOG = db.Column(db.Integer)
    YC = db.Column(db.Integer)
    RC = db.Column(db.Integer)
    GW = db.Column(db.Integer)
    CP = db.Column(db.Integer)
    price = db.Column(db.Integer)
    
    goalkeeper = db.relationship('Goalkeeper', backref='player')

    def __repr__(self):
        return f"<Player (name={self.name!r}, college={self.college!r})>"


class PlayerPrevious(db.Model):

    __tablename__ = "playerprevious"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    college = db.Column(db.String)
    year = db.Column(db.Integer)

    GP = db.Column(db.Integer)
    GS = db.Column(db.Integer)
    MIN = db.Column(db.Integer)
    G = db.Column(db.Integer)
    A = db.Column(db.Integer)
    PTS = db.Column(db.Integer)
    PTS_G = db.Column(db.Float)
    SH = db.Column(db.Integer)
    SH_G = db.Column(db.Float)
    SOG = db.Column(db.Integer)
    YC = db.Column(db.Integer)
    RC = db.Column(db.Integer)
    GW = db.Column(db.Integer)

    CP = db.Column(db.Integer)
    price = db.Column(db.Integer)

    goalkeeper = db.relationship('GoalkeeperPrevious',
                                 backref='playerprevious')

    def __repr__(self):
        return f"<Player (name={self.name!r}, college={self.college!r})>"


class Goalkeeper(db.Model):

    __bind_key__ = None
    """
    GP: games played
    GS: games started
    MIN: minutes played
    GA: goals allowed
    GAA: goals against avg
    PTS: points
    SV: saves
    SV_percentage: saves percentage
    W: wins
    L: losses
    T: ties
    SHO: shootouts
    SF:  shots faced
    """
    """Goalkeeper class"""

    __tablename__ = "goalkeeper"

    # id needs to be the same as in the player database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    college = db.Column(db.String)
    year = db.Column(db.Integer)

    GA = db.Column(db.Integer)
    GAA = db.Column(db.Float)
    PTS = db.Column(db.Integer)
    SV = db.Column(db.Integer)
    SV_percentage = db.Column(db.Float)
    W = db.Column(db.Integer)
    L = db.Column(db.Integer)
    T = db.Column(db.Integer)
    SHO = db.Column(db.Integer)
    SF = db.Column(db.Integer)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

    def __repr__(self):
        return f"<Goalkeeper (id={self.id!r})>"


class GoalkeeperPrevious(db.Model):

    __tablename__ = "goalkeeperprevious"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    college = db.Column(db.String)
    year = db.Column(db.Integer)

    GP = db.Column(db.Integer)
    GS = db.Column(db.Integer)
    MIN = db.Column(db.Integer)
    GA = db.Column(db.Integer)
    GAA = db.Column(db.Float)
    PTS = db.Column(db.Integer)
    SV = db.Column(db.Integer)
    SV_percentage = db.Column(db.Float)
    W = db.Column(db.Integer)
    L = db.Column(db.Integer)
    T = db.Column(db.Integer)
    SHO = db.Column(db.Integer)
    SF = db.Column(db.Integer)

    player_id = db.Column(db.Integer, db.ForeignKey('playerprevious.id'))

    def __repr__(self):
        return f"<Goalkeeper (name={self.id!r})>"


class Fixtures_results(db.Model):

    __tablename__ = "FixturesResults"

    id = db.Column(db.Integer, primary_key=True)
    Parent_index = db.Column(db.Integer)
    Date = db.Column(db.String, nullable=False)
    Away_Team = db.Column(db.String)
    Away_Team_Score = db.Column(db.Integer)
    Home_Team = db.Column(db.String)
    Home_Team_Score = db.Column(db.Integer)
    Location = db.Column(db.String)
    Game_played = db.Column(db.Boolean)


class User(db.Model):

    __tablename__ = "user"

    username = db.Column(db.String, primary_key=True)
    hashed_password = db.Column(db.String)
    
    # The token will change after everytime a user makes a change to their team
    # Once a user signs, the new token is sent to their browser which will be
    # sent for their next request
    token = db.Column(db.Integer)

    userteam = db.relationship('UserTeam', backref='user')


class UserTeam(db.Model):

    __tablename__ = 'userteam'

    username = db.Column(db.String, primary_key=True)
    player1 = db.Column(db.Integer)
    player2 = db.Column(db.Integer)
    player3 = db.Column(db.Integer)
    player4 = db.Column(db.Integer)
    player5 = db.Column(db.Integer)
    total_budget = db.Column(db.Integer)
    used_money = db.Column(db.Integer)

    user_id = db.Column(db.String, db.ForeignKey('user.username'))
