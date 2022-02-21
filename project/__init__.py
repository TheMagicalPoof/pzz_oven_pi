from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO, emit

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
socketio = SocketIO()

def create_app(debug=False):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.signin"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .schedule import schedule as schedule_blueprint
    app.register_blueprint(schedule_blueprint)

    from .settings import settings as settings_blueprint
    app.register_blueprint(settings_blueprint)

    socketio.init_app(app)


    return app
