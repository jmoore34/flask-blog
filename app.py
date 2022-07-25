"""
A small flask application.
Run `flask run` in the directory to start.
"""

from mylib import db_functions, my_forms
from flask import Flask, redirect, render_template, session, request, url_for, Response


app = Flask(__name__)
app.secret_key = "1ccbfc0a11ac4264b771d230fb952b95"


@app.route("/")
@app.route("/home/<message>")
def home(message = None) -> Response:
    """Renders the main homepage with an optional message to the user

    Args:
        message (str, optional): A message to show at the top. Defaults to None.

    Returns:
        Response: the rendered homepage HTML
    """
    return render_template("home.j2", message=message)


@app.route("/admin")
def admin():
    """The admin page which shows the list of users.
    Can only be viewed if the user is a logged in admin.

    Returns:
        Response: content of the admin page (i.e. the list of users)
    """
    if session.get("user") and session["user"]["is_admin"]:
        return render_template("admin.j2", users=db_functions.get_all_users())
    # if not admin, send back to homepage
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = my_forms.RegisterForm()
    if form.validate_on_submit():
        db_functions.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        session["username"] = request.form["username"]
        return redirect(
            url_for(
                "home",
                message=f"Created account successfully. Welcome {session['user']['username']}!",
            )
        )

    return render_template("register.j2", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """The login page, and also the POST endpoint for logging in

    Returns:
        Response | str: a redirect to the main page after logging in, or the HTML of the login page
    """
    form = my_forms.LoginForm()
    if form.validate_on_submit():  # checks that the password is correct
        session["user"] = dict(db_functions.get_user_by_username_or_email(
            form.username_or_email.data
        )) # convert the row to a User dict

        if session["user"]["is_admin"]:
            return redirect(url_for("admin"))

        return redirect(
            url_for(
                "home",
                message=f"Logged in successfully. Welcome back {session['user']['username']}!",
            )
        )

    return render_template("login.j2", form=form)


@app.route("/logout")
def logout():
    """An endpoint which logs the user out and redirects them to the main page

    Returns:
        Response: A redirect to the main page
    """
    session.pop("user")
    return redirect(url_for("home", message="Logged out successfully."))

app.run()
