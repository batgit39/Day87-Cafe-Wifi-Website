from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
Bootstrap(app)
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    map_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField("Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    location = StringField("Cafe Location", validators=[DataRequired()])
    has_sockets = SelectField("Has Sockets", choices=["Yes", "No"], validators=[DataRequired()])
    has_toilet = SelectField("Has Toilet", choices=["Yes", "No"], validators=[DataRequired()])
    has_wifi = SelectField("Has WiFi", choices=["Yes", "No"], validators=[DataRequired()])
    can_take_calls = SelectField("Can Take Calls", choices=["Yes", "No"], validators=[DataRequired()])
    seats = StringField("Number of Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.cafe.data,
            map_url=form.map_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data == "Yes",
            has_toilet=form.has_toilet.data == "Yes",
            has_wifi=form.has_wifi.data == "Yes",
            can_take_calls=form.can_take_calls.data == "Yes",
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    cafes = Cafe.query.all()
    return render_template('cafes.html', cafes=cafes)


if __name__ == '__main__':
    app.run(debug=True)

