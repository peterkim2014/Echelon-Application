from flask import render_template, request, redirect, flash, session
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/welcome_page")
def welcome_page():
    return render_template("welcome_page.html")

@app.route("/login_page")
def login_page():
    return render_template("login_page.html")

@app.route("/register_page")
def register_page():
    return render_template("register_page.html")

@app.route("/create_user", methods=["POST"])
def create_user_form():
    
    if User.validate_registration(request.form):
        data = {
            "username": request.form["username"],
            "email": request.form["email"],
            "password": bcrypt.generate_password_hash(request.form["password"])
        }
        User.create(data)
        flash("Thank you for registering")
        return redirect("login_page"), flash("Thank you for registering")
    else:
        return redirect("register_page")

@app.route("/login_page_form", methods=["POST"])
def login_page_form():

    user = User.get_by_username(request.form["username"])

    if user == None or bcrypt.check_password_hash(user.password, request.form["password"]) == False:
        flash("Invalid Credentials", "login")
        return redirect("login_page")

    session["user_id"] = user.id
    flash("Login Successful")
    return redirect("/homepage")

@app.route("/logout")
def logout():
    flash("Successfully logged out")
    session.clear()
    return redirect("/welcome_page")
