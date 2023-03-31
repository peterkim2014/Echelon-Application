from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, session
from flask_app.models.user import User

class Command:

    dB = "echelon_data"

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
        return cls(result[0] if result else None)
    
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
    def validate_command(command):
        stage = 0
        initial_command = ["open calender","open notes","view","manage","add","edit"]
        calender_command = ["view", "manage", "add", "edit"]

        for index, initial in enumerate(initial_command):
            index += 1
            if command.lower() == initial:
                print(index, "index")     
                return index
        # for index, calender in enumerate(calender_command):
        #     index += 1
        #     if command.lower() == calender:
        #         print(index, "index")     
        #         return index
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

    @classmethod
    def command_list(cls, command):
        path = None
        validation_response = cls.validate_command(command)
        print(validation_response, "validation_response")
        if validation_response == 0 or validation_response == None:
            print("INVALID")
            path = None
            command_prompt = """
                Invalid Response. Please try again!
            """
            return command_prompt, path
        if validation_response == 1:
            print("OPEN CALENDER")
            path = "calender"
            command_prompt = """
                "View or Manage"
            """
            return command_prompt, path
        if validation_response == 2:
            path = "notes"
            print("OPEN NOTES")
            command_prompt = """
                "View or Manage"
            """
            return command_prompt, path
        if validation_response == 3:
            print("VIEW")
            return validation_response
        if validation_response == 4:
            print("MANAGE")
            command_prompt = """
                Choose from one of the following : add, edit, delete.
            """
            return command_prompt
        return False

    @staticmethod
    def command_path(command):
        # initial_command = ["open calender","open notes"]
        calender_command = ["view", "manage", "add", "edit"]
        for index, initial in enumerate(calender_command):
            index += 1
            if command == initial:
                return index
        # for calender in calender_command:
        #     if command == calender:
        #         return "calender"

    @classmethod
    def command_route(cls, command):
        print(command)
        route = cls.command_path(command)
        if route == 1:
            print("open calender")
            return 
        if route == 2:
            print("open notes")
            return 
        return route
