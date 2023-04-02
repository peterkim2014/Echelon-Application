from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, session
from flask_app.models.user import User
from flask_app.models.note import Note

class Command:

    dB = "echelon_data"
    redirect_path = None

    def __init__(self, command_data):
        self.id = command_data["id"]
        self.command = command_data["command"]
        self.created_at = command_data["created_at"]
        self.updated_at = command_data["updated_at"]
        self.user_id = command_data["user_id"]
        self.command_list = []

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO commands (command, user_id) VALUES (%(command)s, %(user_id)s);
        """
        result = MySQLConnection(cls.dB).query_db(query, data)
        return result

    @classmethod
    def create(cls, data):
        cls.save(data)
        return data
    
    @classmethod
    def get_all(cls, id):
        query = """
            SELECT * FROM commands LEFT JOIN users ON commands.user_id = users.id WHERE commands.user_id = %(id)s;
        """
        results = MySQLConnection(cls.dB).query_db(query, {"id":id})
        if results:
            commands_list = []
            for result in results:
                user_data = {
                    "id": result["id"],
                    "username": result["username"],
                    "email": result["email"],
                    "password": None
                }
                input_user = User(user_data)
                command = cls(result)
                command.command_list = input_user
                commands_list.append(command)
            return commands_list
        return None
            

    @classmethod
    def get_one(cls, id):
        query = """
            SELECT * FROM commands WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id":id})
        return cls(result[0]) if result else None
    
    @classmethod
    def delete_command(cls, id):
        query = """
            DELETE FROM commands WHERE id = %(id)s;
        """
        result = MySQLConnection(cls.dB).query_db(query, {"id":id})
        return result
        
    @classmethod
    def validate_user(command):
        is_valid = True
        if User.get_by_id(command.user_id) == User.get_by_username(session["user_username"]):
            return is_valid


    @staticmethod
    def validate_command(input):
        stage = 0
        command_list = ["open calender","open notes","view","manage","add","edit","invalid"]

        for command in command_list:
            if input.lower() == command:
                return stage
            else:
                stage += 1
        for stage in range(0, stage):
            return stage


    @classmethod
    def command_response(cls, commands, id):
        last_command = 0

        for command in commands:
            command_id = command.id
            last_command = command_id
            command_data = Command.get_all(id)

        if command_data:
            command_single = Command.get_one(last_command)

        single_command = command_single.command
        initial_command = cls.command_list(single_command)
        return initial_command
    
    @staticmethod
    def command_path(command):
        path = None
        if command == "open calender":
            path = "/calender/view"
        if command == "open notes":
            path = "/notes/view"
        return path

    @classmethod
    def command_list(cls, input, user_id,redirect_path=redirect_path):
        list = cls.get_all(user_id)
        notes_list = Note.get_all_note_one_user(user_id)
        count = len(list)
        current_id = None
        previous_id = None
        previous_command = None
        current_command = None
        current_id_1 = None
        previous_id_2 = None
        current_id_1_command = None
        previous_id_1_command = None
        previous_id_3_command = None
        notes_list = None
        notes_path = None
        if list:
            if count > 1:
                for data in list:
                    current_id = data.id
                    previous_id = current_id - 1
            if previous_id:
                if current_id:
                    current_data = cls.get_one(current_id)
                    if cls.get_one(previous_id) != None:
                        previous_data = cls.get_one(previous_id)
                        current_command = current_data.command
                        previous_command = previous_data.command

            command_path = cls.command_path(previous_command)
            validation_response = cls.validate_command(input)

            if count > 2:
                for data in list:
                    # add
                    current_id_1 = data.id
                    # manage
                    previous_id_1 = current_id - 1
                    # open calender
                    previous_id_2 = current_id - 2

                if cls.get_one(previous_id_2) != None:
                    current_id_1 = cls.get_one(current_id)
                    previous_id_1 = cls.get_one(previous_id_1)
                    previous_id_2 = cls.get_one(previous_id_2)

                    current_id_1_command = current_id_1.command
                    previous_id_1_command = previous_id_1.command
                    previous_id_2_command = previous_id_2.command

                    notes_list = [current_id_1_command, previous_id_1_command, previous_id_2_command]
                    notes_path = cls.notes_path(notes_list)

        if validation_response == 0:
            command_prompt = """
                "View or Manage"
            """
            return "command",command_prompt
        if validation_response == 1:
            command_prompt = """
                "View or Manage"
            """
            return "command",command_prompt
        if validation_response == 2:
            redirect_path = command_path
            return "redirect",redirect_path
        if validation_response == 3:
            command_prompt = """
                Choose from one of the following : add or edit.
            """
            return "command",command_prompt
        if notes_path == "add":
            command_prompt = """
                Enter your your note and submit
            """
            return "add_note", command_prompt
        return False

    @classmethod
    def notes_path(cls, commands):
        is_add = None
        notes_path = ["open notes", "manage", "add"]
        for command in commands:
            for note in notes_path:
                if command == note:
                    is_add = "add"
        return is_add

