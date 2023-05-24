import requests
from flask import Flask, flash, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = "gaggdf23213241fagwesfsgsq34423gdaedc"

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="admin",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@app.route("/login/", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if username and password:
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                               (str(username), str(password)))
                records = list(cursor.fetchall())
                if records:
                    return render_template('account.html', full_name=records[0][1], login=records[0][2],
                                           password=records[0][3])
                else:
                    flash('Invalid username or password')
                    return render_template('login.html')
            else:
                flash('Username or password is empty')
                return render_template('login.html')
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')


@app.route('/logout/')
def logout():
    return redirect("/login/")


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if name and login and password:
            cursor.execute("SELECT * FROM service.users WHERE login='{l}'".format(l=str(login)))
            records = list(cursor.fetchall())
            if records:
                flash('This username already exists')
            else:
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                               (str(name), str(login), str(password)))
                conn.commit()
                return redirect('/login/')
        else:
            flash('Please fill the form')
    return render_template('registration.html')
