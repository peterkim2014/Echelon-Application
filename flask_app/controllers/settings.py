from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.note import Note
from flask_app.models.calender import Calender
from flask_app.models.command import Command
from flask_app.models.chat import Chat

@app.route("/setting_page")
def settings_page():
    return render_template("main/setting_page.html")