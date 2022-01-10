from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')                #Routing della pagina principale con reindirizzazione al file HTML base da cui
def home():                     #verranno poi estese login.html, prenotazione.html, signup.html attraverso Jinja2 di Flask
    return render_template("base.html")