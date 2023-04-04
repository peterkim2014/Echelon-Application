from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, session
from flask_app.models.user import User

class Calender:
    
    dB = "minute_data"

    def __init__(self, calender_data):
        self.id = calender_data["id"]
        self.event = calender_data["event"]
        self.created_at = calender_data["created_at"]
        self.updated_at = calender_data["updated_at"]
        self.user_id = calender_data["user_id"]
        self.creator = None

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO calenders (event, user_id) VALUES (%(event)s, %(user_id)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)
        return result
    
    @classmethod
    def create(cls, data):
        cls.save(data)
        return data
    
    @classmethod
    def get_all_calender_no_user(cls):
        query = """
            SELECT * FROM calenders;
        """
        result = MySQLConnection(cls.dB).query_db(query)
        return result
    
    @classmethod
    def get_all_calender_one_user(cls, id):
        from flask_app.models.user import User
        query = """
            SELECT * FROM calenders LEFT JOIN users ON calenders.user_id = users.id WHERE calenders.user_id = %(id)s;
        """
        results = MySQLConnection(cls.dB).query_db(query, {"id": id})
        if results:
            calender_list = []
            for result in results:
                user_data = {
                    "id": result["id"],
                    "username": result["username"],
                    "email": result["email"],
                    "password": None
                }
                creator = User(user_data)
                calender = cls(result)
                calender.creator = creator
                calender_list.append(calender)
            return calender_list
        return None

    
    @classmethod
    def get_one_calender(cls, id):
        query = """
            SELECT * FROM calenders WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        return cls(result[0]) if result else None
    
    @classmethod
    def delete(cls, id):
        query = """
            DELETE FROM calenders WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        return result
    
    @staticmethod
    def validate_note(data):
        is_valid = True
        return is_valid, data 

 