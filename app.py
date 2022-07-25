"""
A small flask application.
Run `flask run` in the directory to start.
"""

from flask import Flask, redirect, render_template, session, request, url_for, Response
from mylib import db_functions, my_forms


app = Flask(__name__)
app.secret_key = "1ccbfc0a11ac4264b771d230fb952b95"


@app.route("/")
@app.route("/home/")
@app.route("/home/<message>")
def home(message=None) -> Response:
    """Renders the main homepage with an optional message to the user

    Args:
        message (str, optional): A message to show at the top. Defaults to None.

    Returns:
        Response: the rendered homepage HTML
    """
    return render_template(
        "home.j2", message=message, posts=db_functions.get_all_posts()
    )


@app.route("/about")
def about() -> Response:
    """Renders the about page

    Returns:
        Response: the rendered about page HTML
    """
    return render_template("about.j2")


@app.route("/edit", methods=["GET", "POST"])
@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit(post_id=None):
    """Shows the edit page (for an existing or new post), or the POST endpoint to edit a post

    Args:
        post_id (int, optional): the post's id. Defaults to None.

    Returns:
        Response: edit page HTML or redirect
    """
    if not session.get("user") or not session["user"]["id"]:
        return redirect(url_for("home"))

    existing = None
    if post_id is not None:
        existing = db_functions.get_post(post_id)

    if existing["creator"] != session["user"]["id"] and not session["user"]["is_admin"]:
        return redirect(url_for("home"))

    form = my_forms.EditForm()
    if form.validate_on_submit():
        if existing is None:  # brand new post
            db_functions.create_post(
                title=form.title.data,
                content=form.content.data,
                creator=session["user"]["id"],
            )
            return redirect(url_for("home"))

        # update existing
        db_functions.update_post(
            post_id=post_id, title=form.title.data, content=form.content.data
        )
        return redirect(url_for("home"))

    if existing is not None:
        form.title.data = existing["title"]
        form.content.data = existing["content"]
    return render_template("edit.j2", form=form)


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
    """The register page, as well as POST endpoint to register a user

    Returns:
        Response: the register page HTML or redirect
    """
    form = my_forms.RegisterForm()
    if form.validate_on_submit():
        db_functions.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        session["user"] = dict(
            db_functions.get_user_by_username_or_email(form.username_or_email.data)
        )  # convert the row to a User dict
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
        session["user"] = dict(
            db_functions.get_user_by_username_or_email(form.username_or_email.data)
        )  # convert the row to a User dict

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
