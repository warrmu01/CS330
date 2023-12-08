# Creating/updating databases and csv files

The American Rivers Conference Men's Soccer Tournament runs for about a month or so every year. So, updating and creating new databases can be divides into three different phases:

| Phases | 
| ------------- |
| Before tournament starts  | 
| During the tournament  |
| After the tournament |

The db files used for this fantasy site are :

| DB file  | Info |
| ------------- | ------------- |
| players.db  | All player's data for the latest season. Has two tables : players and goalkeepers  |
| players_previous.db  | All player's data for the previous season. Has two tables : players and goalkeepers   |

The db files are updated/created based on the csv files which are created by the `players_scrape.py` file in the `scrape` directory. The `players_scrape.py` is also reliant on one env variable `LATEST_SEASON`.
https://github.com/paudsu01/AmericanRiversConference-Fantasy/blob/b523cd2f3fe8918c31972b93aede2b2b802bcec0/scrape/.env#L1-L2

Let us look at the different phases and see which databases will be updated in what way:

## Before the tournament starts

After the new rosters are out and a new season is about to start :
* The env variable `LATEST_SEASON` will be incremented by 1.
* The env variable `LATEST_SEASON_ENDED` is set to be false.
* The csv files `goalkeeper_latest.csv` and `player_latest.csv` are renamed to `goalkeeper_previous.csv` and `player_previous.csv`.
* The db file `players.db` is renamed to `players_previous.db`.
* The `players_scrape.py` fetches the data for the latest season creating new `goalkeeper_latest.csv` and `player_latest.csv` files. 
* `create_players_db.py` from inside `db_changes` folder is run to create the db file `players.db`. The `id(PRIMARY_KEY)` of the players for the latest season that were in the previous season is set to be the same.

## During the tournament
After every game of the tournament is played :
* The `players_scrape.py` fetches the current season data and creates(updates) `goalkeeper_latest.csv` and `player_latest.csv`.
* The db file `players.db` is updated if there are any changes.
  
## After the tournament ends
No changes to the database is done nor are any changes necessary. Only the env variable `LATEST_SEASON_ENDED` is set to be true.
