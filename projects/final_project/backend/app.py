from flask import Response, request, render_template
from models import Player, PlayerPrevious, \
    Goalkeeper, GoalkeeperPrevious, \
    User, UserTeam
from models import Fixtures_results

from config import app, db
import json
import sqlalchemy
import bcrypt
import secrets


@app.route('/')
def index():
    return render_template("index.html")


# Different routes
# /players
# /players?name="NAME"
# /players/?data=previous
# /players?name="NAME"&data='previous'
@app.route('/players')
def players():

    type_of_data = request.args.get('data', 'latest')
    dict_of_query = get_dict_query()
    response_list = []

    if type_of_data == 'latest':

        players = Player.query.filter_by(
            **dict_of_query).all()

    else:

        players = PlayerPrevious.query.filter_by(
            **dict_of_query).all()

    for player in players:

        player_dict = {}
        player_dict_copy = player.__dict__
        player_dict.update(player_dict_copy)
        del player_dict['_sa_instance_state']

        response_list.append(player_dict)

    response = Response(json.dumps(response_list), status=200)
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "*"

    return response


def get_dict_query():

    dict_of_query = dict(request.args)
    if 'data' in dict_of_query:
        del dict_of_query['data']

    return dict_of_query


# JOIN is used here to provide data of goalkeepers even from players database
@app.route('/goalkeepers')
def goalkeepers():

    type_of_data = request.args.get('data', 'latest')
    dict_of_query = get_dict_query()
    response_list = []

    if type_of_data == 'latest':

        try:
            goalkeepers = db.session.query(Player, Goalkeeper).join(
                Player, Goalkeeper.player_id == Player.id)\
                .filter_by(**dict_of_query).all()
        except (sqlalchemy.exc.InvalidRequestError):
            goalkeepers = db.session.query(Player, Goalkeeper).join(
                Goalkeeper, Goalkeeper.player_id == Player.id)\
                .filter_by(**dict_of_query).all()

    else:

        try:
            goalkeepers = db.session.query(PlayerPrevious,
                                           GoalkeeperPrevious).join(
                PlayerPrevious,
                GoalkeeperPrevious.player_id == PlayerPrevious.id)\
                .filter_by(**dict_of_query).all()

        except (sqlalchemy.exc.InvalidRequestError):
            goalkeepers = db.session.query(PlayerPrevious, GoalkeeperPrevious)\
                .join(GoalkeeperPrevious,
                      GoalkeeperPrevious.player_id == PlayerPrevious.id)\
                .filter_by(**dict_of_query).all()

    for goalkeeper in goalkeepers:

        goalie_dict = {}
        goalie_dict_0 = goalkeeper[0].__dict__
        goalie_dict_1 = goalkeeper[1].__dict__
        goalie_dict.update(goalie_dict_0)
        goalie_dict.update(goalie_dict_1)
        del goalie_dict['_sa_instance_state']

        response_list.append(goalie_dict)

    response = Response(json.dumps(response_list))
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "*"

    return response


@app.route('/fixtures_results')
def fixtures_results():
    dict_of_query = get_dict_query()

    # Define a list of the 9 teams
    allowed_teams = ['Luther', 'Wartburg', 'Simpson', 'Loras', 'Buena Vista',
                     'Coe', 'Dubuque', 'Central', 'Nebraska Wesleyan',
                     'A-R-C First Round - BYE']

    # Filter fixtures and results where home and away teams
    # are in the allowed teams list
    fixtures_results = Fixtures_results.query.filter(
        Fixtures_results.Home_Team.in_(allowed_teams),
        Fixtures_results.Away_Team.in_(allowed_teams),
        **dict_of_query
    ).all()

    response_list = []

    for fixture_result in fixtures_results:
        fixture_result_dict = {}
        fixture_result_dict_copy = fixture_result.__dict__
        fixture_result_dict.update(fixture_result_dict_copy)
        del fixture_result_dict['_sa_instance_state']

        response_list.append(fixture_result_dict)

    response = Response(json.dumps(response_list), status=200)
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "*"

    return response


# Return the team of a player
@app.route('/user/<string:username>')
def user_data(username: str):
    try:
        # exception if the user doesn't have a team set up yet
        # since list is empty
        user = db.session.query(UserTeam, User).join(
            User,
            UserTeam.username == User.username).filter_by(
            username=username).all()[0]

        user_dict = {}
        user_dict_0 = user[0].__dict__
        user_dict_1 = user[1].__dict__
        user_dict.update(user_dict_0)
        user_dict.update(user_dict_1)
        del user_dict['_sa_instance_state']
        del user_dict['hashed_password']

    # fetch all the player data and use that as the values
    # instead of just player ids
        for value in range(1, 6):

            player_id = user_dict[f"player{value}"]
            player_dict = {}
            player_info_dict = Player.query.filter_by(
                id=player_id).all()[0].__dict__
            player_dict.update(player_info_dict)
            del player_dict['_sa_instance_state']

            user_dict[f"player{value}"] = player_dict

        response = Response(json.dumps(user_dict), status=200)

    except IndexError:
        response = Response(json.dumps({'status': 'error'}), status=404)

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "*"
    return response


@app.route('/changeteam', methods=["POST"])
def changeteam():

    username = request.form.get('username', None)
    token = request.form.get('token', None)
    money_used = request.form.get('money_used', None)
    player_ids = list(map(int, request.form.get('player_ids',
                                                None).split(',')))
    successful = True

    try:
        user_object = User.query.filter_by(
                username=username).all()[0]
        # verify username and token
        if user_object.token != token:
            successful = False
        else:
            # update token
            user_object.token = secrets.token_hex(16)

            user_team_objects = UserTeam.query.filter_by(
                username=username).all()
            if len(user_team_objects) == 1:
                # update the database
                user_team_object = user_team_objects[0]
                user_team_object.player1 = player_ids[0]
                user_team_object.player2 = player_ids[1]
                user_team_object.player3 = player_ids[2]
                user_team_object.player4 = player_ids[3]
                user_team_object.player5 = player_ids[4]
                user_team_object.used_money = money_used

            else:
                user_team_object = UserTeam(
                    username=username,
                    player1=player_ids[0],
                    player2=player_ids[1],
                    player3=player_ids[2],
                    player4=player_ids[3],
                    player5=player_ids[4],
                    total_budget=50,
                    used_money=money_used,
                    user=user_object
                )
                db.session.add(user_team_object)
            db.session.commit()
            
    except IndexError:
        # no such user exists
        successful = False

    if successful:
        # send response back with new token
        dict_ = {
                'status': 'successful',
                'username': username,
                'token': user_object.token
                 }
        response = Response(json.dumps(dict_), status=200)
    else:
        dict_ = {'status': 'unsuccessful'}
        response = Response(json.dumps(dict_), status=400)

    # return the username and the token and the user info
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "*"
    return response


@app.route('/login', methods=["POST"])
def login():
    # Check the user database, if no such username create a new field
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    successful = True

    if username and password:

        user = User.query.filter_by(username=username).all()

        # create the user
        if len(user) == 0:

            user = User(
                username=username,
                hashed_password=hashed,
                token=secrets.token_hex(16)
            )

            db.session.add(user)
            db.session.commit()

        # user already exists
        # check if the password matches
        else:
            # check password and return successful response only
            # if the password is correct
            user = user[0]
            if not bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password):
                successful = False

    # invalid
    else:
        successful = False

    if successful:
        dict_ = {
                'status': 'successful',
                'username': user.username,
                'token': user.token
                 }
        response = Response(json.dumps(dict_), status=200)
    else:
        dict_ = {'status': 'unsuccessful'}
        response = Response(json.dumps(dict_), status=400)

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "*"
    return response
