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
    last_command = 0
    previous_command = last_command - 1
    current_path = None

    command_prompt = "Please enter a command!"
    commands = Command.get_all(user_id)
    
    if commands:
        if Command.command_response(commands, user_id):
            command_prompt = Command.command_response(commands, user_id)
            print(command_prompt)
            if command_prompt == 3:
                for command in commands:
                    command_id = command.id
                    last_command_id = command_id
                last_command = Command.get_one(last_command_id)
                route = Command.command_route(last_command)
                if route == 1:
                    print("view calender")
                Command.delete_command(last_command_id)
                return redirect("/calender/view")
            
            return render_template("notes/home_page.html", command_prompt=command_prompt, commands=commands)
        else:
            command_prompt = Command.command_response(commands, user_id)
            return render_template("notes/home_page.html", command_prompt=command_prompt)
    return render_template("notes/home_page.html", command_prompt=command_prompt)


# second iteration
#  if commands:
#         if command_response:
#             for command in command_response:
#                 if command_prompt == command[0]:
#                     for command in commands:
#                         command_id = command.id
#                         last_command_id = command_id
#                     last_command = Command.get_one(last_command_id)
#                     print(last_command)
#                     route = Command.command_route(last_command)
#                     if route == 1:
#                         print("view calender")
#                     Command.delete_command(last_command_id)
#                     return redirect("/calender/view")
#                 if command_prompt == command_response[1]:
#                     for command in commands:
#                         command_id = command.id
#                         last_command_id = command_id
#                     last_command = Command.get_one(last_command_id)
#                     route = Command.command_route(last_command)
#                     if route == 1:
#                         print("view calender")
#                     Command.delete_command(last_command_id)
#                     return redirect("/calender/view")


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