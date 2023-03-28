import re
from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9,+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:

    dB = "login_system"

    def __init__(self, user_data):
        self.id = user_data["id"]
        self.username = user_data["username"]
        self.email = user_data["email"]
        self.password = user_data["password"]

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data
    
    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM users;
        """
        result = MySQLConnection(cls.dB).query_db(query)
        return result

    @classmethod
    def get_by_id(cls, id):
        query = """
            SELECT * FROM users WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None

    @classmethod
    def get_by_username(cls, username):
        query = """
            SELECT * FROM users WHERE username = %(username)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"username": username})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None

    @classmethod
    def get_by_email(cls, email):
        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"email": email})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None

    @classmethod
    def update_username(cls, id):
        query = """
            UPDATE users SET username = %{username}s WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None

    @classmethod
    def update_email(cls, id):
        query = """
            UPDATE users SET email = %{email}s WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None

    @classmethod
    def update_password(cls, id):
        query = """
            UPDATE users SET password = %{password}s WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        print(cls(result[0]) if result else None)
        return cls(result[0]) if result else None
    
    @classmethod
    def delete(cls, id):
        query = """
            SELECT * FROM users WHERE id = %{id}s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        return result        

    @staticmethod
    def validate_registration(user):
        is_valid = True

        if User.get_by_username(user["username"]) != None:
            is_valid = False
            flash("Username is already used", "registration") #(message, category)
        if len(user["password"]) < 3:
            is_valid = False
            flash("Password is too short", "registration")
        if user["password"] != user["confirm_password"]:
            is_valid = False
            flash("Password does not match", "registration")
        if User.get_by_email(user["email"]):
            is_valid = False
            flash("Email address already used", "registration")
        if not EMAIL_REGEX.match(user["email"]):
            is_valid = False
            flash("Invalid Email Address", "registration")

        return is_valid
