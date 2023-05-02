from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

sql_db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sql_db.sqlite'
    sql_db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    from .model import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .workout import workout as workout_blueprint
    app.register_blueprint(workout_blueprint)

    return app

def create_db_model():
    from . import model
    with create_app().app_context():
        sql_db.create_all()