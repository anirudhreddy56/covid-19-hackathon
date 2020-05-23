from flask import Flask, render_template, request
from flask_mail import Mail, Message
import sqlite3 as sql

app = Flask(__name__)
mail = Mail(app)



conn = sql.connect('database.db')

#
# conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')

@app.route('/')
def home():
    return render_template("index1.html")


@app.route('/donate', methods=['GET', 'POST'])
def donate():
    

    return render_template("donateform.html")


@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        try:
            nm = request.form['first_name']
            donation = request.form['department']
            addr = request.form['address']
            email = request.form['email']
            number = request.form['contact_no']
            password = request.form['password']

            app.config['MAIL_SERVER'] = 'smtp.gmail.com'
            app.config['MAIL_PORT'] = 465
            app.config['MAIL_USERNAME'] = email
            app.config['MAIL_PASSWORD'] = password
            app.config['MAIL_USE_TLS'] = False
            app.config['MAIL_USE_SSL'] = True
            mail = Mail(app)
            with sql.connect("website.db") as con:
                # cur = sql.connect('database.db').cursor()
                cur = con.cursor()
                cur.execute("INSERT INTO donaters (name,donation,address,email,number) VALUES(?, ?, ?, ?, ?)",(nm,donation,addr,email,number) )
                
                cur.execute("select * from donaters")
                rows = cur.fetchall()
                print(rows)
                con.commit()
                print("Record successfully added")
        except:
            con.rollback()
            print("error in insert operation")

        finally:
            msg = Message('Hello ' + nm, sender = 'anirudhreddyb56@gmail.com', recipients = ['anirudhreddy145@gmail.com'])
            msg.body = "Hello this is \t" + nm + "\t i want to donate \t" + donation + "\t this is my address \t" + addr+ "\t my mail id goes with \t" + email+ "\t my contact number \t" + number
            mail.send(msg)
            con.close()

        
        return render_template("sub.html")


app.run(debug=True)
