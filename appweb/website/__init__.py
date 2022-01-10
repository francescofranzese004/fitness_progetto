from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db=SQLAlchemy() #Database utilizzato; Sql-Alchemy
DB_NAME = "database.db" #Il file verrà chiamato in questo modo

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abab'               #Costruiamo l'app, la secret key per il debug
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .view import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')   #Views farà parte delle blueprints per i routing
    app.register_blueprint(auth, url_prefix='/')    #Auth farà parte delle blueprints per i routing

    from .models import User,Prenotazione

    create_database(app) #Qui viene costruito il database di "app"

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  #Incrementatore degli identificativi
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)      #Se il database non esiste, verrà creato quando si farà il check di questa condizione
        print('Database creato.')