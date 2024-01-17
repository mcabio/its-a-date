"""Server for calendar app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)

from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')



@app.route('/new-user', methods=["GET", "POST"])
def register_user():
    """Create new user"""

    if request.method == "GET":
        return render_template('new-user.html')

    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username") 
    fname = request.form.get("first_name")  
    lname = request.form.get("last_name")
    day_start_time = request.form.get("day_start_time")
    day_end_time = request.form.get("day_end_time")
    search_interval_minutes = request.form.get("search_interval_minutes")

    user = crud.get_user_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again")
        return redirect('/new-user')
    else:
        user = crud.create_user(email, 
                                password,  
                                username,
                                fname, 
                                lname, 
                                day_start_time, 
                                day_end_time, 
                                search_interval_minutes)
        db.session.add(user)
        db.session.commit()
        flash("Welcome! Please log in.")
        # return redirect('new-user.html', user_id=user.user_id)
        return redirect('/')



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)