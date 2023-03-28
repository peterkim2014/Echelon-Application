from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, session
from flask_app.models.user import User

class Note:
    
    dB = "echelon_data"

    def __init__(self, notes_data):
        self.id = notes_data["id"]
        self.note = notes_data["note"]
        self.created_at = notes_data["created_at"]
        self.updated_at = notes_data["updated_at"]
        self.user_id = notes_data["user_id"]
        self.creator = None

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO notes (note, user_id) VALUES (%(note)s, %(user_id)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)
        return result
    
    @classmethod
    def create(cls, data):
        cls.save(data)
        return data
    
    @classmethod
    def get_all_notes_no_user(cls):
        query = """
            SELECT * FROM notes;
        """
        result = MySQLConnection(cls.dB).query_db(query)
        return result
    
    @classmethod
    def get_all_note_one_user(cls, id):
        from flask_app.models.user import User
        query = """
            SELECT * FROM notes LEFT JOIN users ON notes.user_id = users.id WHERE notes.user_id = %(id)s;
        """
        results = MySQLConnection(cls.dB).query_db(query, {"id": id})
        if results:
            notes_list = []
            for result in results:
                user_data = {
                    "id": result["id"],
                    "username": result["username"],
                    "email": result["email"],
                    "password": None
                }
                creator = User(user_data)
                note = cls(result)
                note.creator = creator
                notes_list.append(note)
            return notes_list
        return None

    
    @classmethod
    def get_one_note(cls, id):
        query = """
            SELECT * FROM notes WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        return cls(result[0] if result else None)
    
    @classmethod
    def delete(cls, id):
        query = """
            DELETE FROM notes WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id": id})
        return result
    
    @staticmethod
    def validate_note(data):
        is_valid = True
        return is_valid, data 

 