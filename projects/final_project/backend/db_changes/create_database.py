import csv
import os
import sys
import math

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text

sys.path.insert(1, os.path.dirname(os.path.dirname(__file__)))

try:
    from config import db, app
    from models import Player, Goalkeeper, PlayerPrevious, \
        GoalkeeperPrevious, Fixtures_results
except Exception:
    raise Exception()

SQL_DIRECTORY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                  "data/db/")
CSV_DIRECTORY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                  "data/csv/")


def get_player_price(points):
    if points <= 10:
        return 3
    elif 10 < points <= 20:
        return 5
    elif 20 < points <= 30:
        return 8
    elif 30 < points <= 40:
        return 11
    elif 40 < points <= 50:
        return 13
    elif points > 50:
        return 15


def build_goalkeepers_table(session, type_of_table, csv_file_path):

    with open(csv_file_path,
              "r", encoding="utf8") as f:

        goalkeepers = csv.DictReader(f)
        for goalie in goalkeepers:

            saves = int(goalie["SV"])
            points = saves * 2 - int(goalie["GA"])

            if type_of_table == 'previous':

                stmt = sa.select(PlayerPrevious).where(
                    (PlayerPrevious.name == goalie["Player"])
                    & (PlayerPrevious.college == goalie["College"]))

                try:
                    goalkeeper_object = session.execute(stmt).fetchall()[0][0]

                    goalkeeper = GoalkeeperPrevious(
                        id=goalkeeper_object.id,
                        name=goalie["Player"],
                        college=goalie["College"],
                        year=int(goalie["Year"]),
                        GA=int(goalie["GA"]),
                        GAA=float(goalie["GAA"]),
                        PTS=goalkeeper_object.PTS + (points),
                        SV=saves,
                        SV_percentage=float(goalie["SV%"]),
                        W=int(goalie["W"]),
                        L=int(goalie["L"]),
                        T=int(goalie["T"]),
                        SHO=int(goalie["SHO"]),
                        SF=int(goalie["SF"]),
                        playerprevious=goalkeeper_object
                        )
                    goalkeeper_object.PTS = goalkeeper.PTS
                    goalkeeper_object.PTS_G = goalkeeper.PTS /\
                        goalkeeper_object.GP

                    goalkeeper_object.CP = \
                        get_player_price(goalkeeper_object.PTS)

                except IndexError:
                    pass
                # This happens when the player is not in the team roster
                # We only consider goalkeepers in the PLAYERS table

            elif type_of_table == 'latest':

                stmt = sa.select(Player).where(
                    (Player.name == goalie["Player"])
                    & (Player.college == goalie["College"]))

                try:
                    goalkeeper_object = session.execute(stmt).fetchall()[0][0]

                    goalkeeper = Goalkeeper(
                        id=goalkeeper_object.id,
                        name=goalie["Player"],
                        college=goalie["College"],
                        year=int(goalie["Year"]),
                        GA=int(goalie["GA"]),
                        GAA=float(goalie["GAA"]),
                        PTS=goalkeeper_object.PTS + (points),
                        SV=saves,
                        SV_percentage=float(goalie["SV%"]),
                        W=int(goalie["W"]),
                        L=int(goalie["L"]),
                        T=int(goalie["T"]),
                        SHO=int(goalie["SHO"]),
                        SF=int(goalie["SF"]),
                        player=goalkeeper_object
                        )
                    goalkeeper_object.PTS = goalkeeper.PTS
                    goalkeeper_object.PTS_G = goalkeeper.PTS /\
                        goalkeeper_object.GP
                    goalkeeper_object.CP = \
                        get_player_price(goalkeeper_object.PTS)

                except IndexError:
                    pass
                # This happens when the player is not in the team roster
                # We only consider goalkeepers in the PLAYERS table

            session.add(goalkeeper)

        session.commit()


def build_players_table(session, type_of_table, csv_file_path):

    # with open(f"{CSV_DIRECTORY_PATH}/player_latest.csv",
    with open(csv_file_path,
              "r", encoding="utf8") as f:

        players = csv.DictReader(f)
        new_players = []

        for player in players:

            player["MIN"] = int(player["MIN"].split(':')[0])
            player["G"] = int(player["G"])
            player["A"] = int(player["A"])
            player["YC"] = int(player["YC"])
            player["RC"] = int(player["RC"])

            stat_points = (player["G"] * 8) + (player["A"] * 5) -\
                (player["YC"] * 2) - (player["RC"] * 4)
            player["PTS"] = math.ceil(player["MIN"] / 90) * 2 + stat_points
            player["PTS/G"] = player["PTS"] / int(player["GP"])

            if type_of_table == 'previous':

                player_object = PlayerPrevious(
                    name=player["Player"],
                    college=player["College"],
                    year=int(player["Year"]),
                    GP=int(player["GP"]),
                    GS=int(player["GS"]),
                    MIN=player["MIN"],
                    G=player["G"],
                    A=player["A"],
                    PTS=player["PTS"],
                    PTS_G=float(player["PTS/G"]),
                    SH=int(player["SH"]),
                    SH_G=float(player["SH/G"]),
                    SOG=int(player["SOG"]),
                    YC=player["YC"],
                    RC=player["RC"],
                    GW=int(player["GW"]),
                    price=get_player_price(player["PTS"]),
                    CP=get_player_price(player["PTS"])
                    )
                session.add(player_object)

            elif type_of_table == 'latest':

                player_dict = {
                    'name': player["Player"],
                    'college': player["College"]
                               }
                try:
                    with app.app_context():
                        current_player = PlayerPrevious.query.\
                            filter_by(**player_dict).all()[0]

                    player_object = Player(
                        id=current_player.id,
                        name=player["Player"],
                        college=player["College"],
                        year=int(player["Year"]),
                        GP=int(player["GP"]),
                        GS=int(player["GS"]),
                        MIN=player["MIN"],
                        G=player["G"],
                        A=player["A"],
                        PTS=player["PTS"],
                        PTS_G=float(player["PTS/G"]),
                        SH=int(player["SH"]),
                        SH_G=float(player["SH/G"]),
                        SOG=int(player["SOG"]),
                        YC=player["YC"],
                        RC=player["RC"],
                        GW=int(player["GW"]),
                        price=current_player.CP,
                        CP=int(get_player_price(player["PTS"]))
                    )
                except IndexError:
                    new_players.append(player)

                session.add(player_object)

    for player in new_players:

        player_object = Player(

            name=player["Player"],
            college=player["College"],
            year=int(player["Year"]),
            GP=int(player["GP"]),
            GS=int(player["GS"]),
            MIN=player["MIN"],
            G=player["G"],
            A=player["A"],
            PTS=player["PTS"],
            PTS_G=float(player["PTS/G"]),
            SH=int(player["SH"]),
            SH_G=float(player["SH/G"]),
            SOG=int(player["SOG"]),
            YC=player["YC"],
            RC=player["RC"],
            GW=int(player["GW"]),
            price=3,
            CP=int(get_player_price(player["PTS"]))
            )
        session.add(player_object)

    session.commit()


def build_fixtures_results_table(session):

    with open(os.path.join(CSV_DIRECTORY_PATH,
                           "schedule&results.csv"), "r", encoding="utf8") as f:

        fixtures_data = csv.DictReader(f)

        for row in fixtures_data:
            try:
                Away_Team_Score = int(row["Away Team Score"])
            except ValueError:
                Away_Team_Score = 0
            try:
                Home_Team_Score = int(row["Home Team Score"])
            except ValueError:
                Home_Team_Score = 0
            # Adjust the column names and types accordingly
            fixture_result = Fixtures_results(

                Parent_index=row["Parent Index"],
                Date=row["Date"],
                Away_Team=row["Away Team"],
                Away_Team_Score=Away_Team_Score,
                Home_Team=row["Home Team"],
                Home_Team_Score=Home_Team_Score,
                Location=row["Location"],
                Game_played=bool(row["Is Final"])

            )

            session.add(fixture_result)

    session.commit()


def build_db():
    """Initialize the database"""

    db_file_path = os.path.join(SQL_DIRECTORY_PATH, "database.db")

    engine = sa.create_engine(f"sqlite:////{db_file_path}")
    session = scoped_session(sessionmaker(bind=engine))

    for table_name in \
            ['player', 'playerprevious', 'goalkeeper', 'goalkeeperprevious',
             'FixturesResults']:
        sql = text(f'DROP TABLE IF EXISTS {table_name};')
        session.execute(sql)

    db.metadata.create_all(engine)

    # Build database for previous season
    build_players_table(session, 'previous',
                        f"{CSV_DIRECTORY_PATH}/player_previous.csv",)
    build_goalkeepers_table(session, 'previous',
                            f"{CSV_DIRECTORY_PATH}/goalkeeper_previous.csv",)

    # Build database of current season
    build_players_table(session, 'latest',
                        f"{CSV_DIRECTORY_PATH}/player_latest.csv",)
    build_goalkeepers_table(session, 'latest',
                            f"{CSV_DIRECTORY_PATH}/goalkeeper_latest.csv",)

    build_fixtures_results_table(session)
    session.commit()
    session.close()


def main():
    build_db()


if __name__ == "__main__":
    main()
