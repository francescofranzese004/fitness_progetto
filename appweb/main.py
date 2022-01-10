from website import create_app

app = create_app()

if __name__ == '__main__': #Convenzione di denominazione dei file Python
    app.run(debug=True)    #Run dell'app e debug in tempo reale

#Main.py è semplicemente il file che sia accerta che __name__ sia eseguito dalla stessa directory e non eseguito da altrove