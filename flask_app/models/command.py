from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, session
from flask_app.models.user import User

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

        if stage == 0:
            return stage
        if stage == 1:
            return stage
        if stage == 2:
            return stage
        if stage == 3:
            return stage
        if stage == 4:
            return stage
        if stage == 5:
            return stage
        if stage == 6:
            return stage
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
        print(command, "path","*"*20)
        if command == "open calender":
            path = "/calender/view"
        if command == "open notes":
            path = "/notes/view"
        print(path)
        return path

    @classmethod
    def command_list(cls, input, user_id,redirect_path=redirect_path):
        list = cls.get_all(user_id)
        count = len(list)
        current_id = None
        previous_id = None
        previous_command = None
        current_command = None
        if list:
            if count > 1:
                for data in list:
                    current_id = data.id
                    previous_id = current_id - 1
            if previous_id:
                if current_id:
                    current_data = cls.get_one(current_id)
                    print(current_data)
                    if cls.get_one(previous_id) != None:
                        previous_data = cls.get_one(previous_id)
                        current_command = current_data.command
                        previous_command = previous_data.command
        
            print(current_command)
            print(previous_command)

            command_path = cls.command_path(previous_command)
            validation_response = cls.validate_command(input)

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
                Choose from one of the following : add, edit, delete.
            """
            return "command",command_prompt
        return False


