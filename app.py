''' Import the Flask class (to create the web app)
and render_template (to load an HTML file from the templates folder)'''
from flask import Flask, render_template, abort, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

clubs_players = db.Table(
   "clubs_players",
   db.Column(
      "Clubid", db.Integer,
      db.ForeignKey("Clubs.Clubid"),
      primary_key = True
   ),
   db.Column(
      "Playerid", db.Integer,
      db.ForeignKey("Players.Playerid")
   ),
)


class Clubs_Players(db.Model):
 Club_Playersid = db.Column(db.Integer, primary_key=True)

 Playerid = db.Column(
    db.Integer,
    db.ForeignKey("players.Playerid")
)

Clubid = db.Column(
    db.Integer,
    db.ForeignKey("clubs.Clubid")
)
    

class Clubs(db.Model):
   Clubid = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(80), nullable=False)
   Wins = db.Column(db.Integer, nullable=False)
   Losses = db.Column(db.Integer, nullable=False)
   clubs_players = db.relationship(
        "Clubs_Players",
        backref = "clubs"
    )

class Players(db.Model):
    Playerid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    Goals = db.Column(db.Integer, nullable=False)
    Assists = db.Column(db.Integer, nullable=False)
    Saves = db.Column(db.Integer, nullable=False)
    PlayerStartDate= db.Column(db.Date, nullable=False)
    PlayerEndDate= db.Column(db.Date, nullable=False)
    clubs_players = db.relationship(
        "Clubs_Players",
        backref = "players"
    )

class Managers(db.Model):
    Managerid = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), primary_key=True)
    clubs = db.relationship(
        "Clubs",
        backref = "managers"
    )


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pizza.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "BenceJamesRussell"


    db.init_app(app)

   

    @app.route("/clubs")
    def clubs():
        all_clubs = Clubs.query.all()
        return render_template(
            "clubs.html", 
            page_title="Clubs",
            clubs=all_clubs)

    @app.route("/players")
    def players():
        all_players = Players.query.all()
        return render_template("players.html", 
            page_title="Players",
            players=all_players)

    @app.route("/managers")
    def managers():
        all_managers = Managers.query.all()
        return render_template("managers.html", 
            page_title="Players",
            managers=all_managers)
    @app.route("/")
    def root():
        # Load the template file templates/home.html
        # and send extra values into the template:
        # - page_title can be used in the <title> tag (or headings)
        # - greeting can be displayed using {{ greeting }}
        return render_template(
            "home.html", 
            page_title="Home",
            greeting="Kia ora! ORM Connected."
            )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)



































