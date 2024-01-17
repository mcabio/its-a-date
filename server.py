from flask import Flask, render_template, request, flash, redirect, session, make_response
from model import connect_to_db, db
import crud
import os
from jinja2 import StrictUndefined


app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html', user_name=user_name)

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
  
    return render_template('dashboard.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True, threaded=True)