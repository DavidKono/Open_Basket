from flask import Flask, render_template, render_template_string, request, redirect, url_for, jsonify, session

app = Flask(__name__, static_folder='images')
app.secret_key = '32098432039'

import json
import os



@app.route("/")
def home():
    return render_template("home.html")

@app.route('/signin')
def signin():
    return render_template("signin.html")

@app.route('/signin_attempt', methods=['POST'])
def signin_attempt():
    user_name = request.form['user_name']
    password = request.form['password']

    with open('data.json', 'r') as file:
        data = json.load(file)
    user = next((person for person in data['people'] if person['user_name'] == user_name), None)
    if user and user['password'] == password:
        session['user_name'] = user_name  
        session['name'] = user['name']
        session['img_path'] = user['img_path']
        return redirect(url_for('profile', user_name=user_name))
    else:
        content = '<h1>Login Failed</h1><a>Incorrect Password or Username</a>'
        return render_template_string("""
            {% extends "base.html" %}

            {% block content %}
                {{content|safe}}
            {% endblock %}""", content=content)


@app.route('/logout')
def logout():
    session.pop('user_name', None)  
    return redirect(url_for('home'))


@app.route("/profile/<string:user_name>")
def profile(user_name):
    with open('data.json', 'r') as file:
        data = json.load(file)
    user = next((person for person in data['people'] if person['user_name'] == user_name), None)
    if user:
        return render_template("profile.html", user=user)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/about")
def about():
    return render_template("about.html")

def get_charities():
    with open('charities.json', 'r') as file:
        data = json.load(file)
    return data['charities']
@app.route("/charities")
def charities():
    charities = get_charities()
    return render_template("charities.html", charities=charities)

def get_top_donators():
    with open('data.json', 'r') as file:
        data = json.load(file)
    top_donators = sorted(data['people'], key=lambda x: x['weeklyDonation'], reverse=True)[:10]
    return top_donators

@app.route("/leaderboard")
def leaderboard():
    top_donators = get_top_donators()
    return render_template("leaderboard.html", top_donators=top_donators)


""" @app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        return redirect(url_for("user", usr = user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"  """


if __name__ == "__main__":
    app.debug = True
    app.run()

