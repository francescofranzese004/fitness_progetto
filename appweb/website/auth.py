from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User, Prenotazione
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from datetime import datetime

#Il seguente file esegue quelle che sono le funzioni principali della pagina web.
#Contiene i vari routing e redirect a /login - /prenotazione - /signup implementando in ognuno di esse
#i vari form di login, signup e inserimento della prenotazione.


auth = Blueprint('auth', __name__) #Specifico che auth è una collezione di routings appartenente al main


@auth.route('/login', methods=['GET','POST']) #Metodi get e post per l'acquisizione dei dati dalla pagina
def login():
    if request.method == 'POST':
        email = request.form.get('email')   #Prelevo informazioni email dal form
        password = request.form.get('password') #Prelevo informazioni password dal form

        user = User.query.filter_by(email=email).first() #Controllo che l'email esista nella query
        if user: #Se esiste
            if check_password_hash(user.password, password): #Se combaciano le password
                flash('Bentornato!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.prenotazione')) #Login effettuato, redirect alla pagina di prenotazione
            else:
                flash('Password errata, riprovare.', category='error')
        else:
            flash('Email non esistente', category='error')
    return render_template("login.html")    #Le condizoni non si verificano. Si rimane nella pagina di login.


@auth.route('/prenotazione', methods=['GET','POST'])
def prenotazione():
    if request.method=='POST':
        DataOra= datetime.fromisoformat(request.form.get('data') + 'T' + request.form.get('ora')) #Concatenazione. Preleva la data e preleva l'ora dal form
        prenotazione = Prenotazione(DataEOra=DataOra, user_id=current_user.id) #I parametri prenotazione saranno ('Data e ora', 'identificativo utente')
        db.session.add(prenotazione) #Si aggiunge al database
        db.session.commit() #Si aggiorna il database
        flash('Prenotazione effettuata con successo!', category='success')
        print(DataOra)
    return render_template("prenotazione.html")



@auth.route('/sign-up', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')               #^
        password1 = request.form.get('password1')       #|  Raccolta dei dati per
        password2 = request.form.get('password2')       #|  la registrazione dell'account
        nome = request.form.get('nome')                 #v

        user = User.query.filter_by(email=email).first()    #Controlla se esiste già l'email in query

        if user:
            flash('Email già esistente.', category='error')
        elif len(email) < 4:
            flash('L email deve essere maggiore di 4 caratteri.', category='error')
        elif len(nome) < 2:
            flash('Il nome deve essere maggiore di 2 caratteri.', category='error')
        elif password1!=password2:
            flash('Le due password non coincidono', category='error')
        elif len(password1) < 7:
            flash('La password deve essere almeno di 7 caratteri.', category='error')
        else:
            new_user=User(email=email, nome=nome, password=generate_password_hash(password1, method='sha256')) #Parametri di user. La crittografia sha256 fa parte della libreria werkzeug
            db.session.add(new_user)    #Aggiunge l'utente creato
            db.session.commit()         #Aggiorna il database
            login_user(new_user)        #Login
            flash('Utente creato.', category='success')
            return redirect(url_for('auth.prenotazione'))


    return render_template("signup.html")