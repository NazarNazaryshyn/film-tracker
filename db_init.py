from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
import click
from flask.cli import with_appcontext


db = SQLAlchemy()
db_init = Blueprint('db_init', __name__, static_folder='static')


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    """
    It is used to manually create database
    """
    from app import db, User, Film

    db.create_all()


@click.command(name='drop_tables')
@with_appcontext
def drop_tables():
    """
    It is used to manually delete database
    """
    from app import db, User, Film

    db.drop_all()
