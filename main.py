from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from datetime import datetime
import json


with open('config.json', 'r') as c:
    params = json.load(c)["params"]
local_server = True

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['user'],
    MAIL_PASSWORD = params['password']
)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/Devfolio'
mail = Mail(app)
if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']
db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    phone_no = db.Column(db.String(12), nullable = False)
    message = db.Column(db.String(100), nullable = False)
    # date = db.Column(db.String(12))
    date = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def home():
    return render_template('index.html', params=params)

@app.route("/about")
def about():
    return render_template('about.html', params=params)

@app.route("/post")
def post():
    return render_template('post.html', params=params)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        entry = Contacts(name = name, email = email, phone_no = phone, message = message ) 
        db.session.add(entry)       
        db.session.commit()
        mail.send_message('Devsphere: Message from ' + name, 
                          sender = email, 
                          recipients=[params['user']],
                          body =  "\nMail: " + email + "\nPhone no: " + phone+ "\n \n" + message 
                          )
    return render_template('contact.html', params=params)

app.run(debug = True)