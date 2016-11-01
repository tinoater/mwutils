import csv
import os

class Constants():
    def __init__(self, file_path):
        self.file_path = file_path
        self.set_consts_from_file()

    def set_consts_from_file(self):
        """
        Sets global constants from a .const file when of a fixed format

        .const file is a CSV list and is of the form
        <CONST_NAME> , <CONST_TYPE> , <VALUE>
        eg. A_DICT,dictionary,{"Key1":"Value1","Key2":"Value2"}
        :param filepath:
        :return:
        """
        try:
            con_file = open(self.file_path, "r")
        except:
            raise FileNotFoundError("Couldn't open constants text file")

        con_reader = csv.reader(con_file)

        for row in con_reader:
            # First handle any comments and blank lines
            if len(row) == 0:
                continue
            if '#' in row[0]:
                continue

            var_name = row[0]
            var_type = row[1]

            if var_type == 'STRING':
                var_value = ''.join(row[2:])

                # Check that the string starts and ends with a double quote
                if var_value.startswith('"') and var_value.endswith('"'):
                    var_value = var_value[1:-1]
            elif var_type == 'NUMBER':
                try:
                    var_value = float(row[2])
                except:
                    raise Exception(TypeError, "Number should be able to be cast as float")
            elif var_type == 'DICTIONARY':
                # Get a list of the key value pairs
                key_value_pairs = ''.join(row[2:]).replace("{", "").replace("}", "").split(",")

                for key_value_pair in key_value_pairs:
                    var_value = dict()
                    key, value = key_value_pair.split(":")
                    if key.startswith('"'):
                        key = key[1:]
                    if key.endswith('"'):
                        key = key[:-1]

                    if value.startswith('"'):
                        value = value[1:]
                    if value.endswith('"'):
                        value = value[:-1]

                    var_value[key] = value
            else:
                raise Exception(ValueError, "Unknown variable type: " + var_type)

            setattr(self, var_name, var_value)

        con_file.close()
