import json


class JsonReader:
    def __init__(self,file_path):
        self.file_path = file_path
        self.data = {}

    def read_json(self):
        try:
            # Read and parse the JSON file
            with open(self.file_path, "r") as json_file:
                self.data = json.load(json_file)

            # return json data as dictionary
            return self.data

        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {str(e)}")