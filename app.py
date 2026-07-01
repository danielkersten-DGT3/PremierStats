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
    with app.app_context():
        db.create_all()
        if Clubs.query.count() == 0:

            arsenal = Clubs(
                ClubName="Arsenal",
                Wins=20,
                Losses=6
            )

            liverpool = Clubs(
                ClubName="Liverpool",
                Wins=25,
                Losses=4
            )

            mancity = Clubs(
                ClubName="Manchester City",
                Wins=21,
                Losses=7
            )

            chelsea = Clubs(
                ClubName="Chelsea",
                Wins=18,
                Losses=8
            )

            manunited = Clubs(
                ClubName="Manchester United",
                Wins=16,
                Losses=10
            )

            db.session.add_all([
                arsenal,
                liverpool,
                mancity,
                chelsea,
                manunited
            ])
        if Managers.query.count() == 0:
            m_arteta = Managers(Name="Mikel Arteta")
            m_slot = Managers(Name="Arne Slot")
            m_guardiola = Managers(Name="Pep Guardiola")
            m_maresca = Managers(Name="Enzo Maresca")
            m_amorim = Managers(Name="Ruben Amorim")

            db.session.add_all([
                m_arteta,
                m_slot,
                m_guardiola,
                m_maresca,
                m_amorim
            ])
        if Players.query.count() == 0:
            p_saka = Players(
                Name="Bukayo Saka",
                Goals=12,
                Assists=10,
                Saves=0,
                StartDate="2020-09-01",
                EndDate=None
            )

            p_rice = Players(
                Name="Declan Rice",
                Goals=7,
                Assists=8,
                Saves=0,
                StartDate="2023-07-15",
                EndDate=None
            )

            p_haaland = Players(
                Name="Erling Haaland",
                Goals=27,
                Assists=5,
                Saves=0,
                StartDate="2022-07-01",
                EndDate=None
            )

            p_salah = Players(
                Name="Mohamed Salah",
                Goals=24,
                Assists=16,
                Saves=0,
                StartDate="2017-07-01",
                EndDate=None
            )

            p_palmer = Players(
                Name="Cole Palmer",
                Goals=16,
                Assists=11,
                Saves=0,
                StartDate="2023-09-01",
                EndDate=None
            )

            p_onana = Players(
                Name="Andre Onana",
                Goals=0,
                Assists=0,
                Saves=124,
                StartDate="2023-07-20",
                EndDate=None
            )

            p_alisson = Players(
                Name="Alisson Becker",
                Goals=0,
                Assists=1,
                Saves=132,
                StartDate="2018-07-19",
                EndDate=None
            )

            db.session.add_all([
                p_saka,
                p_rice,
                p_haaland,
                p_salah,
                p_palmer,
                p_onana,
                p_alisson
            ])

            db.session.commit()

   

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



































