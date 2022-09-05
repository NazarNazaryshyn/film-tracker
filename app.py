from flask import Flask, request, Blueprint
from functions import *
import os
from flask import render_template, redirect, url_for
from flask_login import current_user, LoginManager
from models import User, Film
from db_init import db,db_init
from authentication import authentication as auth


app = Flask(__name__)


db.init_app(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'movie.db')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


login_manager = LoginManager()
login_manager.login_view = 'authentication.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


db.init_app(app)


app.register_blueprint(db_init)
app.register_blueprint(auth)


@app.route('/', methods=['POST', 'GET'])
def home():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.get_id()).first()
        film_ids = [int(film.film_id) for film in user.films]
    else:
        film_ids = None

    if request.method == 'POST':
        return redirect(url_for('search_results', title=request.form['search_name']))
    cards = form_url('popular_this_day')
    greet_title = 'Popular this day'
    return render_template('home.html', cards=cards, greet_title=greet_title, film_ids=film_ids)


@app.route('/saved_films/')
def saved_films():
    user = User.query.filter_by(id=current_user.get_id()).first()
    cards = [find_film_by_id(int(film.film_id)) for film in user.films]
    film_ids = [int(film.film_id) for film in user.films]

    return render_template('home.html', cards=cards, film_ids=film_ids)


@app.route('/search/<title>')
def search_results(title):
    cards = search_movie(title)
    greet_title = f'Searching results for {title}'
    return render_template('home.html', cards=cards, greet_title=greet_title)


@app.route('/movies/<filter>', methods=['POST', 'GET'])
def home_ext(filter):
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.get_id()).first()
        film_ids = [int(film.film_id) for film in user.films]
    else:
        film_ids = None
    if request.method == 'POST':
        return redirect(url_for('search_results', title=request.form['search_name']))
    cards = form_url(filter)

    while '_' in filter:
        filter = filter.replace('_', ' ')

    return render_template('home.html', cards=cards, greet_title=filter.title(), film_ids=film_ids)


@app.route('/remove_film/<film_id>')
def remove_film(film_id):
    film = Film.query.filter_by(film_id=film_id).first()
    db.session.delete(film)
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/add_film/<film_id>')
def add_film(film_id):

    new_film = Film(
        film_id=film_id,
        owner_id=current_user.get_id()
    )
    db.session.add(new_film)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.debug = True
    app.run()
