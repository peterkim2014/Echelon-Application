from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.note import Note
from flask_app.models.calender import Calender
from flask_app.models.command import Command

@app.route("/calender/view")
def calender_home():
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")
    user = User.get_by_id(session["user_id"])
    all_calender = Calender.get_all_calender_one_user(user.id)
    print(all_calender)
    return render_template("calenders/calender_home.html")

@app.route("/calender/new")
def create_calender_page():
    return render_template("calender/add_calender.html")

@app.route("/calender/new/create", methods=["POST"])
def create_calender_form():
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")
    user_id = session["user_id"]
    data = {
        "event": request.form["calender"],
        "user_id": user_id
    }
    print(data)
    if Calender.validate_note(data):
        Calender.save(data)
        return redirect("/homepage")
    else:
        return redirect("/homepage")

@app.route("/edit/<int:id>")
def edit_calender_page(id):
    calender = Calender.get_by_id(id)
    return render_template("calender/edit_calender.html", calender=calender)

@app.route("/edit/calender", methods=["POST"])
def edit_calender():
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")
    user_id = session["user_id"]
    data = {
        "event": request.form["calender"],
        "user_id": user_id
    }
    
    if Calender.validate_note(data):
        Calender.save(data)
        return redirect("/homepage")
    else:
        return redirect("/homepage")
    
@app.route("/delete/<int:id>")
def delete_calender(id):
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")
    Calender.delete(id)
    return redirect("/homepage")