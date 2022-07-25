"""
A small flask application.
Run `flask run` in the directory to start.
"""

from mylib import db_functions,my_forms
from flask import Flask, redirect, render_template, session, request


app = Flask(__name__)
app.secret_key = "1ccbfc0a11ac4264b771d230fb952b95"


@app.route("/")
def root():
    """The root route, which redirects to the main page

    Returns:
        Response: a redirect to the main page
    """
    return redirect("/main")


# @app.route("/main/")
# def homepage():
#     """The main page

#     Returns:
#         Response: content of the main page
#     """
#     visit_count = int(request.cookies.get("visit_count") or 0)
#     visit_count = visit_count + 1
#     response = make_response(
#         render_template(
#             "main.j2",
#             username=session.get("username"),
#             messages=get_messages(),
#             visit_count=visit_count,
#         )
#     )
#     response.set_cookie("visit_count", bytes(str(visit_count), "utf-8"))
#     return response


@app.route("/register", methods=["GET","POST"])
def register():
    form = my_forms.RegisterForm()
    if form.validate_on_submit():
        db_functions.create_user(username=request.form["username"],
            email=request.form["email"],
            password=request.form["password"]
        )
        session["username"] = request.form["username"]
        return redirect("/")

    return render_template("register.j2", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """The login page, and also the POST endpoint for logging in

    Returns:
        Response | str: a redirect to the main page after logging in, or the HTML of the login page
    """
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect("/main/")

    if "username" in session:  # already logged in
        return redirect("/main")

    return render_template("login.j2")


@app.route("/logout")
def logout():
    """An endpoint which logs the user out and redirects them to the main page

    Returns:
        Response: A redirect to the main page
    """
    session.pop("username")
    return redirect("/main")


@app.route("/about")
def about():
    """The about us page

    Returns:
        Response: The HTML content of the about page
    """
    items = ["Cacti", "Roses", "Dandelions", "Primroses", "Sunflowers", "Tulips"]
    return render_template("about.j2", items=items)


@app.route("/contactus", methods=["GET", "POST"])
@app.route("/contactus/<int:num_contacts>")
def contact(num_contacts=1):
    """A page with a contact form, as well as the POST endpoint to submit the form

    Args:
        num_contacts (int, optional): URL parameter for how many fake phone numbers to show.
         Defaults to 1.

    Returns:
        Response: the HTML of the contact form, or a redirect to the main page if a
         message is submitted
    """
    if (
        request.method == "POST"
        and session.get("username")
        and request.form.get("text")
        and len(request.form["text"]) > 0
    ):

        # add_message(session["username"], request.form["text"])
        return redirect("/main")

    phone_numbers = [
        f"({randint(100,999)})-{randint(100,999)}-{randint(1000,9999)}"
        for i in range(num_contacts)
    ]

    return render_template(
        "contact.j2", phone_numbers=phone_numbers, username=session.get("username")
    )

app.run()