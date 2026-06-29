#planning file - not connected to app
from 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

pizza_topping=db.Table(
"pizza_topping",
db.Column(
    "pizza_id", db.Integer,
    db.ForeignKey("pizza.id"), #points to pizza table
    primary_key=True
),
db.Column(
    "topping_id", db.Integer,
    db.ForeignKey("topping.id"), #points to topping table
    primary_key=True
),
)

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Topping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pizza.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "any-random-string-here"

    db.init_app(app)

    with app.app_context():
        db.create_all()
        if Pizza.query.count() == 0:
            #Create Topping Object
            t_cheese = Topping(name="Cheese")
            t_tomato = Topping(name="Tomato Sauce")
            t_pepperoni = Topping(name="Pepperoni")
            t_ham = Topping(name="Ham")
            t_pineapple = Topping(name="Pineapple")
            t_basil = Topping(name="Basil")              
            db.session.add_all([t_cheese,t_tomato,t_pepperoni,t_ham,t_pineapple, t_basil ])

            #Create Pizza Objects
            p1 = Pizza(name="Margherita", price=12.50)
            p2 = Pizza(name="Hawaiian", price=10.50)
            p3 = Pizza(name="Pepperoni", price=11.50)

            db.session.add_all([p1, p2, p3])

            #Connect Pizza to Topping
            p1.toppings.extend([t_tomato, t_cheese, t_basil])
            p2.toppings.extend([t_tomato, t_cheese, t_ham, t_pineapple])
            p3.toppings.extend([t_tomato, t_cheese, t_pepperoni])

            db.session.commit()
    @app.route("/")
    def root():
        # Load the template file templates/home.html
        # and send extra values into the template:
        # - page_title can be used in the <title> tag (or headings)
        # - greeting can be displayed using {{ greeting }}
        return render_template(
            "home.html", 
            page_title="Home",
            greeting="Kia ora! Jewish ORM Connected."
            )

    #This is the "Pizzas" route
    #When a user visits http://127.0.0.1:5000/pizzas Flask runs this function
    @app.route("/pizzas")
    def pizzas_page():
        pizzas = Pizza.query.order_by(Pizza.name.asc()).all()
        return render_template(
            "pizzas.html",
            page_title = "All Jew Pizzas",
            pizzas = pizzas
            )
    
    @app.route("/pizzas/<int:pizza_id>")
    def pizza_detail(pizza_id):
        pizza = Pizza.query.get(pizza_id)
        if pizza is None:
            abort(404)
        return render_template(
            "pizza_jew.html", 
            page_title=pizza.jew,
            jew=pizza
            )

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)


