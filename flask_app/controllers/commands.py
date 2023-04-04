from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.note import Note
from flask_app.models.calender import Calender
from flask_app.models.command import Command

@app.route("/homepage")
def homepage():
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")

    user_id = session["user_id"]
    last_command = 0
    previous_command = last_command - 1
    all_notes = Note.get_all_note_one_user(user_id)
    all_calender = Calender.get_all_calender_one_user(user_id)
    last_note_id = None
    last_calender_id = None
    
    command_prompt = "Please enter a command!"
    commands = Command.get_all(user_id)
    response_category = None
    response = None
    path = None

    if all_notes:
        for note in all_notes:
            last_note_id = note.id
    if all_calender:
        for calender in all_calender:
            last_calender_id = calender.id
    
    if commands:
        for command in commands:
            command_id = command.id
            last_command_id = command_id

        last_command_data = Command.get_one(last_command_id)
        last_command = last_command_data.command
        response_data = Command.command_list(last_command, user_id)

        if response_data:
            command_data = response_data
            response_category = response_data[0]
            response = response_data[1]

        if response_category == "command":
            command_prompt = response
            return render_template("main/home_page.html", command_prompt=command_prompt, commands=commands)
        if response_category == "redirect":
            path = response
            Command.delete_command(last_command_id)
            if path != None:
                return redirect(path)
            if path == None:
                Command.delete_command(last_command_id)
                return redirect("/homepage")
        if response_category == "add_note":
            command_prompt = response
            Command.delete_command(last_command_id)
            return render_template("main/home_page.html", command_prompt=command_prompt, commands=commands, response_category=response_category)
        if response_category == "edit_note":
            command_prompt = response
            Command.delete_command(last_command_id)
            note = Note.get_one_note(last_note_id)
            return render_template("main/home_page.html", command_prompt=command_prompt, commands=commands, response_category=response_category, note=note)
        if response_category == "add_calender":
            command_prompt = response
            Command.delete_command(last_command_id)
            return render_template("main/home_page.html", command_prompt=command_prompt, commands=commands, response_category=response_category)
        if response_category == "edit_calender":
            command_prompt = response
            Command.delete_command(last_command_id)
            calender = Calender.get_one_calender(last_calender_id)
            return render_template("main/home_page.html", command_prompt=command_prompt, commands=commands, response_category=response_category, calender=calender)


        return render_template("main/home_page.html", command_prompt=command_prompt, commands=commands)

    return render_template("main/home_page.html", command_prompt=command_prompt)


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