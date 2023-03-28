from flask_app import app
from flask_app.controllers import users, application

if __name__=="__main__":
    app.run(debug=True)