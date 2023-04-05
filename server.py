from flask_app import app
from flask_app.controllers import users, notes, commands, calenders, minutes, abouts, settings

if __name__=="__main__":
    app.run(debug=True)