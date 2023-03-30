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

        for initial in initial_command:
            last_command = len(initial_command)
            stage += 1
            if command.lower() == initial:
                print(stage)
                return stage
            return stage

        return stage

    @classmethod
    def command_response(cls, commands):
        for command in commands:
            command_id = command.id
            command_data = Command.get_one(command_id)
            single_command = command_data.command
            print(single_command)
            initial_command = cls.command_list(single_command)
            return initial_command

    @classmethod
    def command_list(cls, command):
        initial_command = [
            "open calender", "open notes", "view", "manage"
        ]

        for initial in initial_command:
            if cls.validate_command(command) == 0:
                command_prompt = """
                    Invalid Response. Please try again!
                """
                return command_prompt
            if cls.validate_command(command) == 1:
                command_prompt = """
                    "View or Manage"
                """
                return command_prompt
            if cls.validate_command(command) == 2:
                command_prompt = """
                    "View or Manage"
                """
                return command_prompt
            if cls.validate_command(command) == 4:
                command_prompt = """
                    Choose from one of the following : add, edit, delete.
                """
                return command_prompt
        return False













            # if Command.start_command(single_command.command) == True:
            #     command_prompt = "View or Manage"
            #     if command_prompt == "open calender":
            #         if command_prompt == "view" or command_prompt == "View":
            #             return redirect("/calender/view") 
            # if Command.initial_response(single_command.command) == True:
            #     if single_command.command == "View" or single_command.command == "view":
            #         command_prompt = """
            #             This is the list of your notes. If you would like to manage your notes. Type "manage"
            #         """
            #     if single_command.command == "Manage" or single_command.command == "manage":
            #         command_prompt = """
            #             To edit, choose from one of the following : Add, Update, Delete.
            #         """
            #     if single_command.command == "Add" or single_command.command == "add":
            #         command_prompt = """
            #             Please enter your note. Press enter to submit.
            #         """
            #         if single_command.command != None:
            #             pass
            #     # Need to work on connecting which note to update
            #     if single_command.command == "Update" or single_command.command == "update":
            #         command_prompt = """
            #             Which note would you like to update?
            #         """ 
            #     if single_command.command == "Delete" or single_command.command == "delete":
            #         command_prompt = """
            #             Which note would you like to delete?
            #         """
            # else:
            #     command_prompt = "Invalid Response. Please Try Again!"