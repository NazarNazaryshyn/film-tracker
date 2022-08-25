# from flask import Flask
# import os
# # from extensions import db, migrate
# import extensions
# from flask_login import LoginManager
#
#
# def create_app():
#
#     app = Flask(__name__)
#     basedir = os.path.abspath(os.path.dirname(__file__))
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'movie.db')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SECRET_KEY'] = 'fakfkafk30f2afkakk2fafa'
#
#     extensions.db.init_app(app)
#     extensions.migrate.init_app(app, extensions.db)
#
#     login_manager = LoginManager()
#     login_manager.login_view = 'authentication.login'
#     login_manager.init_app(app)
#
#     # from .models import User
#     import models
#     @login_manager.user_loader
#     def load_user(user_id):
#         return models.User.query.get(int(user_id))
#
#     from authentication import authentication as auth_register
#     app.register_blueprint(auth_register)
#
#     from db_init import db_init as db_register
#     app.register_blueprint(db_register)
#
#     from main import main_app as main_register
#     app.register_blueprint(main_register)
#
#     return app
