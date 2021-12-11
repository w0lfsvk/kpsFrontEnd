from re import S
from flask import Flask, render_template, request, send_file, url_for, flash, redirect
import csv
from pathlib import Path
import smtplib
from email.message import EmailMessage

from flask.helpers import flash
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'



database_csv = "database.csv"
if not Path(database_csv).exists():
    Path(database_csv).touch()

@app.route("/",methods=["POST"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        mail = request.form["mail"]
        phone = request.form["phone"]
        message = request.form["message"]
        data = [name, mail, phone, message]

        
        server = smtplib.SMTP("smtp.gmail.com", port=587)
        server.starttls()
        server.login(config.email,config.password)


        msg= EmailMessage()
        msg.set_content("Meno: "+name+"\n"+"Tel. č: "+phone+"\n"+"Mail: "+mail+"\n"+message)

        msg["Subject"] = "Dopyt Web "+name
        msg["From"] = config.email
        msg["To"] = config.email

        server.send_message(msg)
        server.quit()

        with open(database_csv, 'a', newline='',encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows([data])
        if request.form['buttonTest'] == 'submit':
            flash("Správa bola úspešne odoslaná")
            return redirect(request.url)
    return render_template("/index.html")
        
@app.route("/")
@app.route("/index")
def index():
    return render_template("/index.html")

@app.route("/contact")
def contact():
    return render_template("/contact.html")

@app.route("/news")
def news():
    return render_template("/news.html")

if __name__=="__main__":
    app.debug= True
    app.run(host="0.0.0.0")
