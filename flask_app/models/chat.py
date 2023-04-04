from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, session
from flask_app.models.user import User

class Chat:

    dB = "minute_data"

    def __init__(self, chats_data):
        self.id = chats_data["id"]
        self.chat = chats_data["chat"]
        self.user_id = chats_data["user_id"]

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