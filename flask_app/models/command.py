from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash, session
from flask_app.models.user import User
from flask_app.models.note import Note

class Command:

    dB = "minute_data"
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


    @classmethod
    def validate_command(cls, input):
        stage = 0
        command_list = ["open calender","open notes","view","manage","add","edit","invalid"]
        
        for command in command_list:
            if input == command:
                return stage
            else:
                stage += 1
        for stage in range(0, stage):
            return stage

    
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
        commands_list = cls.get_all(user_id)
        count = len(commands_list)
        current_id_commands = None
        previous_id_commands = None
        current_command = None
        previous_command = None
        current_id_1 = None
        previous_id_2 = None
        current_id_1_command = None
        previous_id_1_command = None
        notes_list = None
        notes_path = None
        if commands_list:
            if count > 1:
                for index, data in enumerate(commands_list):
                    if index == 0:
                        previous_id_commands = data.id
                    if index == 1:
                        current_id_commands = data.id
            if previous_id_commands:
                if current_id_commands:
                    current_data = cls.get_one(current_id_commands)
                    if cls.get_one(previous_id_commands) != None:
                        previous_data = cls.get_one(previous_id_commands)
                        current_command = current_data.command
                        previous_command = previous_data.command

            command_path = cls.command_path(previous_command)
            if input:
                validation_response = cls.validate_command(input)
            else:
                validation_response = cls.validate_command(current_command)

            if count > 2:
                for index, data in enumerate(commands_list):
                    if index == 0:
                        # add
                        current_id_1 = data.id
                    if index == 1:
                        # manage
                        previous_id_1 = data.id
                    if index == 2:
                        # open calender
                        previous_id_2 = data.id

                if cls.get_one(previous_id_2) != None:
                    get_one_id_1 = cls.get_one(current_id_1)
                    get_one_id_2 = cls.get_one(previous_id_1)
                    get_one_id_3 = cls.get_one(previous_id_2)

                    current_id_1_command = get_one_id_1.command
                    previous_id_1_command = get_one_id_2.command
                    previous_id_2_command = get_one_id_3.command

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
        if notes_path == "note_add":
            print("add prompt")
            command_prompt = """
                Enter your note and submit
            """
            return "add_note", command_prompt
        if notes_path == "note_edit":
            command_prompt = """
                Edit your note and submit
            """
            return "edit_note", command_prompt
        if notes_path == "calender_add":
            print("add prompt")
            command_prompt = """
                Enter your event and submit
            """
            return "add_calender", command_prompt
        if notes_path == "calender_edit":
            command_prompt = """
                Edit your event and submit
            """
            return "edit_calender", command_prompt
        return False

    @classmethod
    def notes_path(cls, commands):
        is_path = None
        note_path = "open notes"

        calender_path = "open calender"
        notes_add = ["open notes", "manage", "add"]
        notes_edit = ["open notes", "manage", "edit"]
        calenders_add = ["open calender", "manage", "add"]
        calenders_edit = ["open calender", "manage", "edit"]

        for command in commands:
            for note_add in notes_add:
                if command == note_add:
                    is_path = "note_add"
                
                for note_edit in notes_edit:
                    if command == note_edit:
                        is_path = "note_edit"
            
                    for calender_add in calenders_add:
                        if command == calender_add:
                            is_path = "calender_add"
                            
                        for calender_edit in calenders_edit:
                            if command == calender_edit:
                                is_path = "calender_edit"
                 
        print(commands)
        print(is_path)
                    
        return is_path

