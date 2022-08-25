from flask import url_for, render_template, Blueprint, redirect
from flask_login import login_user, logout_user
from models import User, LoginForm, RegisterForm
from db_init import db
from werkzeug.security import check_password_hash, generate_password_hash


authentication = Blueprint('authentication', __name__, static_folder='static')


@authentication.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
    return render_template('login.html', form=form)


@authentication.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        password=hashed_password,
                        email=form.email.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('authentication.login'))

    return render_template('register.html', form=form)


@authentication.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('authentication.login'))