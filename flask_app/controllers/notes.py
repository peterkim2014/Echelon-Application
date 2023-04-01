from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.note import Note

@app.route("/notes/view")
def view_note():
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")
    user = User.get_by_id(session["user_id"])
    return render_template("notes/view_note.html", user=user)

@app.route("/note/new")
def create_note_page():
    return render_template("notes/add_note.html")

@app.route("/note/new/create", methods=["POST"])
def create_note_form():
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")

    data = {
        "note": request.form["note"],
        "user_id": request.form["user_id"]
    }
    if Note.validate_note(data):
        Note.save(data)
        return redirect("/homepage")
    else:
        return redirect("/homepage")

@app.route("/edit/<int:id>")
def edit_note_page(id):
    note = Note.get_by_id(id)
    return render_template("notes/edit_note.html", note=note)

@app.route("/edit/note", methods=["POST"])
def edit_note():
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")
    data = {
        "note": request.form["note"],
        "user_id": request.form["user_id"]
    }
    
    if Note.validate_note(data):
        Note.save(data)
        return redirect("/homepage")
    else:
        return redirect("/homepage")
    
@app.route("/delete/<int:id>")
def delete_note(id):
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")
    Note.delete(id)
    return redirect("/homepage")

@app.route("/like/<int:id>")
def like_note(id):
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")
    data = {
                "user_id": session["user_id"],
                "note_id": id
            }

    is_liked = Note.get_many_id(session["user_id"])
    if is_liked:
        for note in is_liked:
            print(note.id)
            print(id)
            if Note.check_like(data) == False:
                print("LIKED")
                Note.like(data)
                return redirect("/homepage")
            else:
                print("ALREADY LIKED")
    else:
        print("Added to DB")
        Note.like(data)
    return redirect("/homepage")
    

@app.route("/unlike/<int:id>")
def unlike_note(id):
    if not "user_id" in session:
        flash("Please Log In", "login")
        return redirect("/login_page")
    data = {
        "user_id": session["user_id"],
        "note_id": id
    }
    if Note.get_one_with_likes(session["user_id"]) != None:
        Note.unlike(data)
        print("unliked")
        return redirect("/homepage")
    return redirect("/homepage")