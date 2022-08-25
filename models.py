from flask_login import UserMixin
from flask_wtf import FlaskForm
from sqlalchemy import Column, Integer, String
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from db_init import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    films = db.relationship('Film', backref='user')


class Film(db.Model):
    id = Column(Integer, primary_key=True)
    film_id = Column(Integer)
    owner_id = Column(Integer, db.ForeignKey('user.id'))


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(),
                                       Length(min=4, max=20)],
                           render_kw={'placeholder': 'Username'})

    email = StringField(validators=[InputRequired(),
                                    Length(min=4, max=50)],
                        render_kw={'placeholder': 'Email'})

    password = PasswordField(validators=[InputRequired(),
                                         Length(min=4, max=20)],
                             render_kw={'placeholder': 'Password'})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(),
                                       Length(min=4, max=20)],
                           render_kw={'placeholder': 'Username'})

    password = PasswordField(validators=[InputRequired(),
                                         Length(min=4, max=20)],
                             render_kw={'placeholder': 'Password'})

    submit = SubmitField('Login')