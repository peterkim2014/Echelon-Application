from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.note import Note
from flask_app.models.command import Command

@app.route("/homepage")
def homepage():
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")

    user_id = session["user_id"]

    command_prompt = "Please enter a command!"
    commands = Command.get_all(user_id)
    if commands:
        if Command.command_response(commands):
            command_prompt = Command.command_response(commands)
            return render_template("notes/home_page.html", command_prompt=command_prompt, commands=commands)
        else:
            command_prompt = Command.command_response(commands)
            return render_template("notes/home_page.html", command_prompt=command_prompt)
        
    return render_template("notes/home_page.html", command_prompt=command_prompt)

@app.route("/create_command", methods=["POST"])
def create_command_form():
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")

    user = User.get_by_id(session["user_id"])
    
    data = {
        "command": request.form["search_input"],
        "user_id": user.id
    }
    # need to validate data before posting data
    Command.create(data)
    return redirect("/homepage")

@app.route("/delete_command", methods=["POST"])
def delete_command():
    command_id = request.form["id"]
    delete_command = Command.delete_command(command_id)
    return redirect("/homepage")

@app.route("/refresh", methods=["POST"])
def delete_all_commands():
    commands = Command.get_all(session["user_id"])
    if commands:
        for command in commands:
            print(command.id)
            Command.delete_command(command.id)
            print("DELETED")
        return redirect("/homepage")

    return redirect("/homepage")