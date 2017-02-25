from bs4 import BeautifulSoup
from contextlib import closing
from selenium import webdriver
import time
import os
import psutil

import mwutils.config as config


class Constants():
    def __init__(self, file_path):
        self.file_path = file_path
        self.set_consts_from_file()

    def set_consts_from_file(self):
        """
        Sets global constants from a .const file when of a fixed format

        .const file is a CSV list and is of the form
        <CONST_NAME> , <CONST_TYPE> , <VALUE>
        eg. A_DICT,DICTIONARY,{"Key1":"Value1","Key2":"Value2"}

        Can force an end of file witht the line END_OF_FILE
        :param filepath: First looks in local directory, then takes the full path
        :return:
        """
        try:
            con_file = open(self.file_path, "r")
        except FileNotFoundError:
            try:
                con_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), self.file_path))
            except:
                raise FileNotFoundError("Couldn't open constants text file")

        i = 0
        loop = True
        while loop:
            row = con_file.readline()
            # First handle any comments and blank lines
            if len(row) == 0:
                loop = False
                continue
            if '#' in row[0] or row == "\n":
                continue
            if row[:11] == 'END_OF_FILE':
                loop = False
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
                        if row[0] != '#':
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
                if var_value.endswith('}\n'):
                    var_value_temp = var_value[:-2]
                elif var_value.endswith('\n'):
                    var_value_temp = var_value[1:-1]
                    while not (row.endswith('}\n') or row.endswith('}')):
                        row = con_file.readline()
                        if row[0] != '#':
                            # Strip out any left padding
                            row = row.lstrip()
                            var_value_temp += row.replace('\n', '')
                else:
                    var_value_temp = var_value

                key_value_pairs = var_value_temp.replace("{", "").replace("}", "").split(",")

                var_value = dict()
                for key_value_pair in key_value_pairs:
                    first_colon = key_value_pair.find(':')
                    key = key_value_pair[:first_colon]
                    value = key_value_pair[first_colon + 1:]
                    if key.startswith('"'):
                        key = key[1:]
                    if key.endswith('"'):
                        key = key[:-1]

                    if value.startswith(" "):
                        value = value[1:]
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    else:
                        value = float(value)

                    var_value[key] = value

            else:
                raise Exception(ValueError, "Unknown variable type: " + var_type)

            setattr(self, var_name, var_value)

        con_file.close()


def get_page_source_url(url, webdriver_path, out_file_path=None, sleep_time=5, class_to_poll=None):
    """
    Get page html (including javascript generated elements)
    If a css_selector is passed in then this selector is polled up to SELENIUM_IMPLICIT_WAIT seconds
    After this a one second sleep time is applied
    If a css_selector is not pased in then sleep_time is applied
    :param url: Full url (including http://)
    :param out_file_path: Full path to output file (if wanted)
    :param sleep_time: Time in seconds to wait for JS to load
    :return: BeautifulSoup object
    """
    with closing(webdriver.Chrome(webdriver_path)) as browser:
        # Set the max element wait timeout
        browser.implicitly_wait(config.SELENIUM_IMPLICIT_WAIT)

        browser.get(url)
        # wait for the page to load
        if class_to_poll is not None:
            test = browser.find_elements_by_class_name(class_to_poll)
            time.sleep(2)
        else:
            time.sleep(sleep_time)

        # Page wait has finished, now save page source
        page_source = browser.page_source.encode("ascii", errors="ignore").decode()
        current_url = browser.current_url

    html_soup = BeautifulSoup(page_source, "lxml")
    html_soup.requested_url = url
    html_soup.final_url = current_url

    if out_file_path is not None:
        if not os.path.exists(os.path.dirname(out_file_path)):
            os.makedirs(os.path.dirname(out_file_path))
        out_file = open(out_file_path, "w")
        out_file.write(page_source)
        out_file.close()

    return html_soup


def get_page_source_file(file_path):
    """
    Return html soup from a html text file
    :param file_path:
    :return: BeautifulSoup object
    """
    with open(file_path) as my_file:
        html = my_file.read()
        html_soup = BeautifulSoup(html, "lxml")

    return html_soup


def get_page_source(file_path=None, url=None, sleep_time=5, ignore_files=False, webdriver_path=config.WEBDRIVER_PATH,
                    class_to_poll=None):
    """
    Gets the BeautifulSoup from either a file (if its specified) or a website if it is not
    :param file_path:
    :param url:
    :param sleep_time:
    :param ignore_files:
    :return:
    """
    if file_path is not None:
        from_file = True
    else:
        from_file = False

    if url is not None:
        from_url = True
    else:
        from_url = False

    if ignore_files:
        from_file = False
        from_url = True

    if from_file:
        # Check if the file_path exists
        try:
            html_soup = get_page_source_file(file_path)
            return html_soup
        except FileNotFoundError:
            if not from_url:
                raise FileNotFoundError("File not found, specify URL instead")

    if from_url:
        html_soup = get_page_source_url(url, webdriver_path, out_file_path=file_path, sleep_time=sleep_time,
                                        class_to_poll=class_to_poll)
        return html_soup
    else:
        return None


def get_active_processes_by_name(process_name):
    """
    Return processes that match the given process_name
    :param process_name: Exact name of processes to be found
    :return: List of process objects
    """
    found_processes = []
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name"])
        except psutil.NoSuchProcess:
            pass
        else:
            if pinfo["name"] == process_name:
                # Add to the list
                found_processes.append(proc)

    return found_processes


def kill_processes(process_list):
    """
    Kill each process in a list

    :param process_list: psutil.Process object list
    :return:
    """
    for p in process_list:
        p.kill()


def kill_processes_by_name(process_name):
    """
    Kill processes that match the process name
    :param process_name: Exact name of processes to be found
    :return: Number of killed processes
    """
    process_list = get_active_processes_by_name(process_name)
    number_of_processes = len(process_list)

    if number_of_processes > 0:
        kill_processes(process_list)

    return number_of_processes
