"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    # queries for all user objects, set to a variable to pass into the html page

    return render_template("user_list.html", users=users)


@app.route('/registration')
def show_reg_form():
    """Renders registration_form page for users to fill out"""

    return render_template("registration_form.html")


@app.route('/processed_form')
def process_form():
    """Get information that the user filled in, check if email exists in database"""

    email = request.args.get('email')
    password = request.args.get('pass')

    if User.query.filter(User.email==email).first():
    # Query the database for the email entered, if it exists already redirect back
    # to the form page

        flash("Sorry, that email already exists.")

        return redirect('/registration')

    else:
    # if the user does not exist...

        newuser = User()
        # instantiate the User class

        db.session.add(newuser)
        # add the user to the database session

        newuser.email = email
        # set the email to the input email

        db.session.commit()
        # commit the session

        flash('else !')

        return render_template("new_page.html", newuser=newuser)


@app.route('/login_form', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('pass')

    print('EMAILLLLL!!!!!!!', email)

    if User.query.filter(User.email==email).first():
        print('Yeaaaaaaahh, you in derr')
        return render_template('new_page.html')

    else:
        print('else, SORRY')
        return redirect('/registration')






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    # DEBUG_TB_INTERCEPT_REDIRECTS = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
