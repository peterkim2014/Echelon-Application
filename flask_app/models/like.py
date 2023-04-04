from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, session
from flask_app.models.user import User

class Like:

    db = "minute_data"

    def __init__(self, likes_data):
        self.id = likes_data["id"]
        self.user_id = likes_data["user_id"]
        self.chat_id = likes_data["chat_id"]
        self.user_data = []
        self.chat_data = []
        self.user_likes_list = []
        self.chat_likes_list = []

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO likes (user_id, chat_id) VALUES (%(user_id)s, %(chat_id)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)
        return result
    
    @classmethod
    def create(cls, data):
        cls.save(data)
        return data

    @classmethod
    def get_all(cls, data):
        from flask_app.models.user import User
        from flask_app.models.chat import Chat
        query = """
            SELECT * FROM likes
            LEFT JOIN users
            ON users.id = likes.user_id
            LEFT JOIN chats
            ON chats.id = likes.chat_id
        """
        results = MySQLConnection(cls.dB).query_db(query)
        if results:
            likes_list = []
            for result in results:
                chat = {
                    "id": result["id"]
                    "chat": result["chat"]
                    "user_id": result["chats.user_id"]
                }
                user = {
                    "id": result["id"]
                    "username": result["username"]
                    "email": result["email"]
                    "password": None
                }
                user_data = User(user)
                chat_data = Chat(chat)
                like = cls(result)
                like.user_data = user_data
                like.chat_data = chat_data
                likes_list.append(like)
            return likes_list
        return None

    @classmethod
    def get_by_user_id(cls, id):
        query = """
            SELECT * FROM likes
            LEFT JOIN users
            ON users.id = likes.user_id
            LEFT JOIN chats
            ON chats.id = likes.chat_id
            WHERE likes.user_id = %(id)s
        """
        results = MySQLConnection(cls.dB).query_db(query, {"id": id})
        if result:
            user_likes_list = []
            for result in results:
                chat = {
                    "id": result["id"]
                    "chat": result["chat"]
                    "user_id": result["chats.user_id"]
                }
                user = {
                    "id": result["id"]
                    "username": result["username"]
                    "email": result["email"]
                    "password": None
                }
                user_data = User(user)
                chat_data = Chat(chat)
                like = cls(result)
                like.user_data = user_data
                like.chat_data = chat_data
                user_likes_list.append(like)
            return user_likes_list
        return None

    @classmethod
    def get_by_chat_id(cls, id):
        query = """
            SELECT * FROM likes
            LEFT JOIN users
            ON users.id = likes.user_id
            LEFT JOIN chats
            ON chats.id = likes.chat_id
            WHERE likes.chat_id = %(id)s
        """
        results = MySQLConnection(cls.dB).query_db(query, {"id": id})
        if result:
            chat_likes_list = []
            for result in results:
                chat = {
                    "id": result["id"]
                    "chat": result["chat"]
                    "user_id": result["chats.user_id"]
                }
                user = {
                    "id": result["id"]
                    "username": result["username"]
                    "email": result["email"]
                    "password": None
                }
                user_data = User(user)
                chat_data = Chat(chat)
                like = cls(result)
                like.user_data = user_data
                like.chat_data = chat_data
                chat_likes_list.append(like)
            return chat_likes_list
        return None
