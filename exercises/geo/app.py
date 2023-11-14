import requests
import records 
from flask import Flask, request, render_template, send_from_directory
from flask import redirect, url_for
import sqlite3
import pathlib

app = Flask(__name__)

def get_data_from_db(query: str, host: str = "localhost", port: int = 2345, user: str = "warrmu01", dbname: str = "world") -> list:
    """Retrieve data from the database and return to the user"""
    db = records.Database(f"postgresql://{user}:@{host}:{port}/{dbname}")

    try:
        rows = db.query(query)
        rows.all()  
        return rows.all()  
    except Exception as e:
        print(f"Error executing query: {e}")
        raise 

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # display links to 3 options (country / region / continent)
        return render_template("index.html")
    # retrieve data from the database based on the selected option and present it to the user
    if request.method == "POST":
        print("Form submitted with data:", request.form)
        if request.form.get("selcountry"):
            country = request.form.get("selcountry")
            results = get_data_from_db(
                host="localhost",
                port=2345,
                user="warrmu01",
                dbname="world",
                query=f"select * from country where code = '{country}';",
            )
            return render_template("country.html", rows=results)
        
        elif request.form.get("selregion"):
            region = request.form.get("selregion")
            results = get_data_from_db(
                host="localhost",
                port=2345,
                user="warrmu01",
                dbname="world",
                query=f"SELECT * FROM country WHERE region = '{region}';",
            )
            return render_template("region.html", rows=results)

        elif request.form.get("selcontinent"):
            continent = request.form.get("selcontinent")
            results = get_data_from_db(
                host="localhost",
                port=2345,
                user="warrmu01",
                dbname="world",
                query=f"select * from country where continent = '{continent}' AND population > 0;",
            )
            return render_template("continent.html", rows=results)
        return "Invalid form submission"

@app.route("/<string:scope>")
def search(scope: str):
    if scope == "country":
        # get countries from the database and populate options of the drop-down menu
        results = get_data_from_db(
            host="localhost",
            port=2345,
            user="warrmu01",
            dbname="world",
            query="select name,code from country"
        )
        return render_template("country.html", options=results)
        
    elif scope == "region":
        # get regions from the database and populate options of the drop-down menu
        results = get_data_from_db(
            host="localhost",
            port=2345,
            user="warrmu01",
            dbname="world",
            query="select DISTINCT region FROM country;"
        )
        print(results)
        return render_template("region.html", options=results)
       
    elif scope == "continent":
        # get continents from the database and populate options of the drop-down menu
        results = get_data_from_db(
            host="localhost",
            port=2345,
            user="warrmu01",
            dbname="world",
            query="select DISTINCT continent FROM country;"
        )
        print(results)
        return render_template("continent.html", options=results)

if __name__ == "__main__":
    db_dir = "."
    with records.Database(f"sqlite:///{pathlib.Path(db_dir) / 'world.sqlite3'}") as conn:
        app.run(debug=True)
