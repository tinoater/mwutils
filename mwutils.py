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

        #con_reader = csv.reader(con_file)

        i = 0
        loop = True
        while loop:
            row = con_file.readline()
            # First handle any comments and blank lines
            if len(row) == 0:
                loop = False
                continue
            if '#' in row[0]:
                continue

            # Pull out the first and second arguments, the rest is the variable value
            first_comma = row.find(',')
            second_comma = row.find(',', first_comma + 1)
            var_name = row[0:first_comma]
            var_type = row[first_comma + 1: second_comma]
            var_value = row[second_comma + 1:]

            if var_type == 'STRING':
                # Handles the single line case
                if var_value.startswith('"') and var_value.endswith('"\n'):
                    var_value = var_value[1:-2]
                elif var_value.startswith('"') and var_value.endswith('\n'):
                    var_value = var_value[1:]
                    # We need to continue until we find the end of this string
                    while not (row.endswith('"\n') or row.endswith('"')):
                        row = con_file.readline()
                        var_value += row
                    # Remove the trailing characters
                    if row.endswith('"\n'):
                        var_value = var_value[:-2]
                    elif row.endswith('"'):
                        var_value = var_value[:-1]

            elif var_type == 'NUMBER':
                try:
                    var_value = float(var_value)
                except:
                    raise Exception(TypeError, "Number should be able to be cast as float")

            elif var_type == 'DICTIONARY':
                # Handles the single line case
                if var_value.startswith('"') and var_value.endswith('}\n'):
                    var_value_temp = var_value[1:-2]
                elif var_value.startswith('"') and var_value.endswith('\n'):
                    var_value_temp = var_value[1:-1]
                    while not (row.endswith('}\n') or row.endswith('}')):
                        row = con_file.readline()
                        var_value_temp += row.replace('\n', '')
                else:
                    var_value_temp = var_value

                key_value_pairs = var_value_temp.replace("{", "").replace("}", "").split(",")

                var_value = dict()
                for key_value_pair in key_value_pairs:
                    key, value = key_value_pair.split(":")
                    if key.startswith('"'):
                        key = key[1:]
                    if key.endswith('"'):
                        key = key[:-1]

                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    else:
                        value = float(value)

                    var_value[key] = value

            else:
                raise Exception(ValueError, "Unknown variable type: " + var_type)

            setattr(self, var_name, var_value)

        con_file.close()
