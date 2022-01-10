from . import db    #Importanzione del database costruito
from flask_login import UserMixin  #Funzionalità riguardanti login e identificazione dell'user


class Prenotazione(db.Model):   #Classe Prenotazione del db
    id = db.Column(db.Integer, primary_key=True)    #Identificativo prenotazione
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))  #Identificativo user
    DataEOra=db.Column(db.DateTime, nullable = False)   #Colonna riguardante Data e Orario prenotazione


class User(db.Model, UserMixin):    #Classe Utente del db
    id = db.Column(db.Integer, primary_key=True)    #Identificativo utente
    email = db.Column(db.String(150), unique=True)  #Colonna E-mail inserite dagli utenti
    password = db.Column(db.String(150))    #Colonna delle password
    nome = db.Column(db.String(150))        #...Nomi
    prenot = db.relationship('Prenotazione')    #Specifica che c'è relazione fra le due classi