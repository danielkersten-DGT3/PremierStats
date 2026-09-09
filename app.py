''' Import the Flask class (to create the web app)
and render_template (to load an HTML file from the templates folder)'''
from flask import Flask, render_template, abort, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
db = SQLAlchemy()

#Tables
clubs_players = db.Table(
    "clubs_players",
    db.Column("Clubid", db.Integer, db.ForeignKey("clubs.Clubid"), primary_key=True),
    db.Column("Playerid", db.Integer, db.ForeignKey("players.Playerid"), primary_key=True),
)

class Clubs(db.Model):
    Clubid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    Wins = db.Column(db.Integer, nullable=False)
    Losses = db.Column(db.Integer, nullable=False)
    Managerid = db.Column(
    db.Integer,
    db.ForeignKey("managers.Managerid")
)       

    players = db.relationship(
        "Players",
        secondary=clubs_players,
        back_populates="clubs"
    )

class Players(db.Model):
    Playerid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    Goals = db.Column(db.Integer, nullable=False)
    Assists = db.Column(db.Integer, nullable=False)
    Saves = db.Column(db.Integer, nullable=False)
    PlayerStartDate = db.Column(db.Date, nullable=False)
    PlayerEndDate = db.Column(db.Date, nullable=False)

    clubs = db.relationship(
        "Clubs",
        secondary=clubs_players,
        back_populates="players"
    )

class Managers(db.Model):
    Managerid = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), nullable=False)
    clubs = db.relationship(
    "Clubs",
    backref="manager"
)

class Users(db.Model):
    Userid = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(80), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(200), nullable=False)
    Admin = db.Column(db.Boolean, default=False)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///football.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "BenceJamesRussell"

    #info for tables
    db.init_app(app)
    with app.app_context():
        db.create_all()
        if Clubs.query.count() == 0:

            arsenal = Clubs(
                name="Arsenal",
                Wins=20,
                Losses=6
            )

            liverpool = Clubs(
                name="Liverpool",
                Wins=25,
                Losses=4
            )

            mancity = Clubs(
                name="Manchester City",
                Wins=21,
                Losses=7
            )

            chelsea = Clubs(
                name="Chelsea",
                Wins=18,
                Losses=8
            )

            manunited = Clubs(
                name="Manchester United",
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
            arsenal.manager = m_arteta
            liverpool.manager = m_slot
            mancity.manager = m_guardiola
            chelsea.manager = m_maresca
            manunited.manager = m_amorim

        if Players.query.count() == 0:
                p_saka = Players(
                    name="Bukayo Saka",
                    Goals=12,
                    Assists=10,
                    Saves=0,
                    PlayerStartDate=datetime(2020, 9, 1),
                    PlayerEndDate=datetime(2030, 6, 30)
                )

                p_rice = Players(
                    name="Declan Rice",
                    Goals=7,
                    Assists=8,
                    Saves=0,
                    PlayerStartDate=datetime(2023, 7, 15),
                    PlayerEndDate=datetime(2028, 6, 30)
                )

                p_haaland = Players(
                    name="Erling Haaland",
                    Goals=27,
                    Assists=5,
                    Saves=0,
                    PlayerStartDate=datetime(2022, 7, 1),
                    PlayerEndDate=datetime(2030, 6, 30)
                )

                p_salah = Players(
                    name="Mohamed Salah",
                    Goals=24,
                    Assists=16,
                    Saves=0,
                    PlayerStartDate=datetime(2017, 7, 1),
                    PlayerEndDate=datetime(2027, 6, 30)
                )

                p_palmer = Players(
                    name="Cole Palmer",
                    Goals=16,
                    Assists=11,
                    Saves=0,
                    PlayerStartDate=datetime(2023, 9, 1),
                    PlayerEndDate=datetime(2030, 6, 30)
                )

                p_onana = Players(
                    name="Andre Onana",
                    Goals=0,
                    Assists=0,
                    Saves=124,
                    PlayerStartDate=datetime(2023, 7, 20),
                    PlayerEndDate=datetime(2028, 6, 30)
                )

                p_alisson = Players(
                    name="Alisson Becker",
                    Goals=0,
                    Assists=1,
                    Saves=132,
                    PlayerStartDate=datetime(2018, 7, 19),
                    PlayerEndDate=datetime(2027, 6, 30)
                )
                p_martinelli = Players(
                    name="Gabriel Martinelli",
                    Goals=8,
                    Assists=6,
                    Saves=0,
                    PlayerStartDate=datetime(2019, 7, 1),
                    PlayerEndDate=datetime(2027, 6, 30)
                )

                p_odegaard = Players(
                    name="Martin Odegaard",
                    Goals=6,
                    Assists=9,
                    Saves=0,
                    PlayerStartDate=datetime(2021, 8, 20),
                    PlayerEndDate=datetime(2028, 6, 30)
                )

                p_saliba = Players(
                    name="William Saliba",
                    Goals=2,
                    Assists=1,
                    Saves=0,
                    PlayerStartDate=datetime(2019, 7, 25),
                    PlayerEndDate=datetime(2027, 6, 30)
                )

                p_van_dijk = Players(
                    name="Virgil van Dijk",
                    Goals=3,
                    Assists=2,
                    Saves=0,
                    PlayerStartDate=datetime(2018, 1, 1),
                    PlayerEndDate=datetime(2027, 6, 30)
                )

                p_diaz = Players(
                    name="Luis Diaz",
                    Goals=10,
                    Assists=5,
                    Saves=0,
                    PlayerStartDate=datetime(2022, 1, 30),
                    PlayerEndDate=datetime(2027, 6, 30)
                )

                p_mac_allister = Players(
                    name="Alexis Mac Allister",
                    Goals=5,
                    Assists=6,
                    Saves=0,
                    PlayerStartDate=datetime(2023, 7, 1),
                    PlayerEndDate=datetime(2028, 6, 30)
                )

                p_foden = Players(
                    name="Phil Foden",
                    Goals=14,
                    Assists=8,
                    Saves=0,
                    PlayerStartDate=datetime(2017, 7, 1),
                    PlayerEndDate=datetime(2028, 6, 30)
                )

                p_de_bruyne = Players(
                    name="Kevin De Bruyne",
                    Goals=5,
                    Assists=10,
                    Saves=0,
                    PlayerStartDate=datetime(2015, 8, 30),
                    PlayerEndDate=datetime(2025, 6, 30)
                )

                p_ruben_dias = Players(
                    name="Ruben Dias",
                    Goals=2,
                    Assists=1,
                    Saves=0,
                    PlayerStartDate=datetime(2020, 9, 29),
                    PlayerEndDate=datetime(2027, 6, 30)
                )

                p_nicolas_jackson = Players(
                    name="Nicolas Jackson",
                    Goals=9,
                    Assists=4,
                    Saves=0,
                    PlayerStartDate=datetime(2023, 7, 1),
                    PlayerEndDate=datetime(2030, 6, 30)
                )

                p_enzo = Players(
                    name="Enzo Fernandez",
                    Goals=4,
                    Assists=7,
                    Saves=0,
                    PlayerStartDate=datetime(2023, 1, 31),
                    PlayerEndDate=datetime(2031, 6, 30)
                )

                p_madueke = Players(
                    name="Noni Madueke",
                    Goals=6,
                    Assists=3,
                    Saves=0,
                    PlayerStartDate=datetime(2023, 1, 23),
                    PlayerEndDate=datetime(2030, 6, 30)
                )

                p_bruno = Players(
                    name="Bruno Fernandes",
                    Goals=10,
                    Assists=9,
                    Saves=0,
                    PlayerStartDate=datetime(2020, 1, 30),
                    PlayerEndDate=datetime(2027, 6, 30)
                )

                p_garnacho = Players(
                    name="Alejandro Garnacho",
                    Goals=7,
                    Assists=5,
                    Saves=0,
                    PlayerStartDate=datetime(2022, 7, 1),
                    PlayerEndDate=datetime(2028, 6, 30)
                )

                p_mainoo = Players(
                    name="Kobbie Mainoo",
                    Goals=3,
                    Assists=2,
                    Saves=0,
                    PlayerStartDate=datetime(2023, 1, 1),
                    PlayerEndDate=datetime(2028, 6, 30)
                )

                p_isak = Players(
                    name="Alexander Isak",
                    Goals=15,
                    Assists=4,
                    Saves=0,
                    PlayerStartDate=datetime(2022, 8, 26),
                    PlayerEndDate=datetime(2028, 6, 30)
                )

                p_gordon = Players(
                    name="Anthony Gordon",
                    Goals=8,
                    Assists=6,
                    Saves=0,
                    PlayerStartDate=datetime(2023, 1, 1),
                    PlayerEndDate=datetime(2029, 6, 30)
                )

                p_son = Players(
                    name="Son Heung-min",
                    Goals=12,
                    Assists=8,
                    Saves=0,
                    PlayerStartDate=datetime(2015, 8, 28),
                    PlayerEndDate=datetime(2026, 6, 30)
                )

                p_maddison = Players(
                    name="James Maddison",
                    Goals=7,
                    Assists=8,
                    Saves=0,
                    PlayerStartDate=datetime(2023, 7, 1),
                    PlayerEndDate=datetime(2028, 6, 30)
                )

                db.session.add_all([
                    p_saka,
                    p_rice,
                    p_haaland,
                    p_salah,
                    p_palmer,
                    p_onana,
                    p_alisson,
                    p_martinelli,
                    p_odegaard,
                    p_saliba,
                    p_van_dijk,
                    p_diaz,
                    p_mac_allister,
                    p_foden,
                    p_de_bruyne,
                    p_ruben_dias,
                    p_nicolas_jackson,
                    p_enzo,
                    p_madueke,
                    p_bruno,
                    p_garnacho,
                    p_mainoo,
                    p_isak,
                    p_gordon,
                    p_son,
                    p_maddison
                ])
                arsenal.players.extend([
                p_saka,
                p_rice,
                p_martinelli,
                p_odegaard,
                p_saliba
                ])

                liverpool.players.extend([
                        p_salah,
                        p_alisson,
                        p_van_dijk,
                        p_diaz,
                        p_mac_allister
                    ])

                mancity.players.extend([
                        p_haaland,
                        p_foden,
                        p_de_bruyne,
                        p_ruben_dias
                    ])

                chelsea.players.extend([
                        p_palmer,
                        p_nicolas_jackson,
                        p_enzo,
                        p_madueke
                    ])

                manunited.players.extend([
                        p_onana,
                        p_bruno,
                        p_garnacho,
                        p_mainoo
                    ])

                db.session.commit()

   

    @app.route("/clubs")
    def clubs():
        search = request.args.get("search", "")

        if search:
            all_clubs = Clubs.query.filter(
                Clubs.name.ilike(f"%{search}%")
            ).all()
        else:
            all_clubs = Clubs.query.all()

        return render_template(
            "Clubs.html", 
            page_title="Clubs",
            clubs=all_clubs)


    @app.route("/players")
    def players():
        search = request.args.get("search", "")

        if search:
            all_players = Players.query.filter(
                Players.name.ilike(f"%{search}%")
            ).all()
        else:
            all_players = Players.query.all()

        return render_template(
            "players.html",
            page_title="Players",
            players=all_players,
            search=search
        )
    
    @app.route("/managers")
    def managers():
        search = request.args.get("search", "")

        if search:
            all_managers = Managers.query.filter(
                Managers.Name.ilike(f"%{search}%")
            ).all()
        else:
            all_managers = Managers.query.all()
        return render_template("managers.html", 
            page_title="Managers",
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
    @app.route("/manager/<int:Managerid>")
    def manager(Managerid):
        manager = Managers.query.get_or_404(Managerid)
        return render_template(
            "manager.html",
            manager=manager
        )
    @app.route("/player/<int:Playerid>")
    def player(Playerid):

        player = Players.query.get_or_404(Playerid)

        return render_template(
            "player.html",
            page_title=player.name,
            player=player
        )

    @app.route("/club/<int:Clubid>")
    def club(Clubid):
        club = Clubs.query.get_or_404(Clubid)

        return render_template(
            "club.html",
            page_title=club.name,
            club=club
        )
    
    @app.route("/add_player", methods=["GET", "POST"])
    def add_player():
        clubs = Clubs.query.all()
        if request.method=="POST":
            name = request.form["name"]
            goals = request.form["goals"]
            assists = request.form["assists"]
            saves = request.form["saves"]
            start_date = datetime.strptime(
                request.form["start_date"],
                "%Y-%m-%d").date()
            end_date = datetime.strptime(
                request.form["end_date"],
                "%Y-%m-%d").date()

            #Find the selected club
            club = Clubs.query.get(
                request.form["club"]
        )
            new_player = Players(
            name=name,
            Goals=goals,
            Assists=assists,
            Saves=saves,
            PlayerStartDate=start_date,
            PlayerEndDate=end_date
        )
            #Connect player to club
            new_player.clubs.append(club)
            db.session.add(new_player)
            db.session.commit()

            return redirect(url_for("players"))
        return render_template(
        "add_player.html",
        page_title="Add Player",
        clubs=clubs
        )


    
    @app.route("/profile")
    def profile():
        #Stores User's Info
        if "userid" not in session:
            return redirect(url_for("login"))

        user = Users.query.get(session["userid"])

        if user is None:
            return redirect(url_for("login"))

        return render_template(
            "profile.html",
            username=user.Username,
            email=user.Email
            Admin=user.Admin
    )

    @app.route("/delete_player/<int:Playerid>", methods=["POST"])
    def delete_player(Playerid):
        player = Players.query.get_or_404(Playerid)

        db.session.delete(player)
        db.session.commit()
        

        return redirect(url_for("players"))


    @app.route("/login", methods=["GET", "POST"])
    def login():
        #Requests username, password and email
        #If successful sends them to profile
        #If not gives them error message
        if request.method == "POST":

            login_input = request.form["login"]
            password = request.form["password"]

            user = Users.query.filter(
                (Users.Username == login_input) |
                (Users.Email == login_input)
            ).first()

            if user and check_password_hash(user.Password, password):

                session["username"] = user.Username
                session["userid"] = user.Userid
                session["admin"] = user.Admin

                return redirect(url_for("profile"))

            return render_template(
                "login.html",
                error="Incorrect username/email or password"
            )

        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        #Creates User Infor and stores it in database
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]

                # Check if username already exists
            existing_user = Users.query.filter_by(
                    Username=username
                ).first()

            if existing_user:
                    return render_template(
                        "register.html",
                        error="Username already exists"
                    )

                # Check if email already exists
            existing_email = Users.query.filter_by(
                    Email=email
                ).first()

            if existing_email:
                    return render_template(
                        "register.html",
                        error="Email already exists"
                    )

            if username == "Admin":
                Admin = True
            else:
                Admin = False

            # Create new user
            hashed_password = generate_password_hash(password)
            new_user = Users(
                    Username=username,
                    Email=email,
                    Password=hashed_password
                )

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        return render_template("register.html")



    @app.route("/logout")
    def logout():
        #User Log out
        session.pop("username", None)
        return redirect(url_for("root"))
    return app



app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)



