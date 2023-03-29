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
        for command in commands:
            command_id = command.id
            if command_id != None:
                single_command = Command.get_one(command_id)
                if single_command != None:
                    command_prompt = """
                        Invalid Response. Please try again!
                    """
            if Command.start_command(single_command.command) == True:
                command_prompt = "View or Manage"
            if Command.initial_response(single_command.command) == True:
                if single_command.command == "View" or single_command.command == "view":
                    command_prompt = """
                        This is the list of your notes. If you would like to manage your notes. Type "manage"
                    """
                if single_command.command == "Manage" or single_command.command == "manage":
                    command_prompt = """
                        To edit, choose from one of the following : Add, Update, Delete.
                    """
                if single_command.command == "Add" or single_command.command == "add":
                    command_prompt = """
                        Please enter your note. Press enter to submit.
                    """
                    if single_command.command != None:
                        pass
                # Need to work on connecting which note to update
                if single_command.command == "Update" or single_command.command == "update":
                    command_prompt = """
                        Which note would you like to update?
                    """ 
                if single_command.command == "Delete" or single_command.command == "delete":
                    command_prompt = """
                        Which note would you like to delete?
                    """
            else:
                command_prompt = "Invalid Response. Please Try Again!"
        return render_template("notes/home_page.html", command_prompt=command_prompt, commands=commands)
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

