from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234Abd'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{yourPassword}@localhost/electronic_store'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .control import control
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(control, url_prefix='/')

    from .models import Employee,Customer

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user_type = session.get('user_type')
        if user_type == 'employee':
            return Employee.query.get(int(user_id))
        elif user_type == 'customer':
            return Customer.query.get(int(user_id))
        return None
    return app
