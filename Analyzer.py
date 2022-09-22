from argparse import ArgumentParser
from abc import ABC, abstractmethod
from collections import Counter
import json
import sys
import pdb


class OutputLoader(object):
    def __init__(self, output_path):
        self.output = str(output_path)

    def get_output(self):
        return self.output


#The input parameter 'operation' of the class Json_output_Loader, is an object of an operation class which contains
#the returned data, and name of the class
class Json_output_Loader(OutputLoader):
    def __init__(self, output_path, operation):
        OutputLoader.__init__(self, output_path)

        try:
            data_output_dict: dict = dict()
            data_output_dict[operation.name] = operation.data_output
            with open(self.get_output(), 'w') as json_file:
                json.dump(data_output_dict, json_file)
        except OSError as err:
            print("OS Error: {0}".format(err))
            print("Provide a correct output file")
            sys.exit(1)
        except ValueError:
            print("Could not convert data")
            sys.exit(1)
        except TypeError:
            print("Unable to serialize the object")
            sys.exit(1)
        except Exception as e:
            print("Error: %s", str(e))
            print("Exception occurred. Exiting...")
            sys.exit(1)

# Base class. It will store common input for any existing loader (other formats)
class LogsLoader(object):
    def __init__(self, data_input):
        #This attribute store the path of the input file. It will be a common attribute for all the inherited classes
        self._input = str(data_input)

    def get_input(self):
        return self._input


# Class in charge of loading an input file, and run the appropiate method according to the log formats
# Here only CSV format is taken into account
class CSV_Loader(LogsLoader):
    def __init__(self, data_input):
        LogsLoader.__init__(self, data_input)
        self.field_1: list = list()
        self.field_2: list = list()
        self.field_3: list = list()
        self.field_4: list = list()
        self.field_5: list = list()
        self.field_6: list = list()
        self.field_7: list = list()
        self.field_8: list = list()
        self.field_9: list = list()
        self.field_10: list = list()
        self.csv_decode()

    def csv_decode(self):
        # with open(super()._input, 'r') as file:
        try:
            with open(self.get_input(), 'r') as file:
                line_text = file.readline()
                line_number = 0
                fields_list: list = list()
                while line_text:
                    fields_list = line_text.split(' ')
                    if len(fields_list) < 10:       #This is to skip blank lines of the file
                        line_text = file.readline()
                        continue
                    self.field_1.append(fields_list[0])
                    del fields_list[0]
                    while fields_list[0] == '':
                        del fields_list[0]          #Remove spaces between first and second field

                    self.field_2.append(fields_list[0])
                    self.field_3.append(fields_list[1])
                    self.field_4.append(fields_list[2])
                    self.field_5.append(fields_list[3])
                    self.field_6.append(fields_list[4])
                    self.field_7.append(fields_list[5])
                    self.field_8.append(fields_list[6])
                    self.field_9.append(fields_list[7])
                    self.field_10.append(fields_list[8])

                    line_number += 1
                    line_text = file.readline()

        except OSError as err:
            print("OS Error: {0}".format(err))
            print("Provide a correct input file. It must be placed in the same folder as the script")
            sys.exit(1)
        except ValueError:
            print("Could not convert data")
            sys.exit(1)
        except Exception as e:
            print("Error: %s", str(e))
            print("Exception occurred. Exiting...")
            sys.exit(1)

        print("LOG: Number of lines in input file: ", line_number)


#  The Operation interface declares a method action() for building the inherited classes.
# Future operations (inherited classes) must contain an action() method to implement the new funcionality and return a string
class Operation(ABC):
    @abstractmethod
    def action(self, request) -> str:
        pass


class MostFrequentIP(Operation):
    def __init__(self, LogsLoader):
        self.LogsLoader = LogsLoader
        self.data_output = self.action()        #Will be used as the value of the returned json
        self.name = self.__class__.__name__     #Will be used as the key of the returned json

    def action(self):
        try:
            counter = Counter(self.LogsLoader.field_3)
            ordered_elements = counter.most_common()
            first = ordered_elements[0]
            
        except Exception as e:
            print("Error: %s", str(e))
            print("Exception occurred. Exiting...")
            sys.exit(1)

        return str(first[0])


class LeastFrequentIP(Operation):
    def __init__(self, LogsLoader):
        self.LogsLoader = LogsLoader
        self.data_output = self.action()  # Will be used as the value of the returned json
        self.name = self.__class__.__name__  # Will be used as the key of the returned json

    def action(self):
        try:
            counter = Counter(self.LogsLoader.field_3)
            ordered_elements = counter.most_common()
            last = ordered_elements[-1]
        except Exception as e:
            print("Error: %s", str(e))
            print("Exception occurred. Exiting...")
            sys.exit(1)

        #There are more ip with 1 occurence. In this version we will take only one of them
        return str(last[0])


#This will return the average number of frames/sec
class EventsperSecond(Operation):
    def __init__(self, LogsLoader):
        self.LogsLoader = LogsLoader
        self.data_output = self.action()  # Will be used as the value of the returned json
        self.name = self.__class__.__name__  # Will be used as the key of the returned json

    def action(self):
        try:
            timestamp_sec = self.remove_decimal_part()
            counter = Counter(timestamp_sec)
            ordered_elements = counter.most_common()

            number_occurences = 0
            number_elements = 0
            for element in ordered_elements:
                number_occurences = number_occurences + element[1]
                number_elements = number_elements + 1

            events_per_sec = number_occurences/number_elements
        except Exception as e:
            print("Error: %s", str(e))
            print("Exception occurred. Exiting...")
            sys.exit(1)

        return events_per_sec

    def remove_decimal_part(self):
        timestamp_sec: list = list()
        for timestamp in self.LogsLoader.field_1:
            timestamp_sec.append(timestamp.split('.')[0])

        return timestamp_sec


# I will assume that total amount of bytes of each log, is the sum of the header size(field 2) and the body size (field 5)
class TotalAmountofBytes(object):
    def __init__(self, LogsLoader):
        self.LogsLoader = LogsLoader
        self.data_output = self.action()  # Will be used as the value of the returned json
        self.name = self.__class__.__name__  # Will be used as the key of the returned json

    def action(self):
        try:
            header_bytes_accumulated = 0
            for header_bytes in self.LogsLoader.field_2:
                header_bytes_accumulated = header_bytes_accumulated + int(header_bytes)

            body_bytes_accumulated = 0
            for body_bytes in self.LogsLoader.field_5:
                body_bytes_accumulated = body_bytes_accumulated + int(body_bytes)
        except Exception as e:
            print("Error: %s", str(e))
            print("Exception occurred. Exiting...")
            sys.exit(1)

        return header_bytes_accumulated + body_bytes_accumulated


def parse_arguments():

    # Load script arguments.

    parser = ArgumentParser(description='Script to analyze logs for SwissRe')

    parser.add_argument('-i', '--input', default=None, help='Path to a plain text which contain logs')
    parser.add_argument('-o', '--output', default=None, help='Path to a file to save output in plain text JSON format')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-m', '--most_frequent', action='store_true', help='Most frequent IP')
    group.add_argument('-l', '--least_frequent', action='store_true', help='Least frequent IP')
    group.add_argument('-e', '--events_second', action='store_true', help='Events per second')
    group.add_argument('-t', '--total_bytes', action='store_true', help='Total Bytes')

    args = parser.parse_args()

    return args


def main():

    params = parse_arguments()

    if (params.input and params.output) is not None:
        input_path = params.input
        output_path = params.output
    else:
        print('Input and Output arguments are mandatories. Please re-introduce them')
        return False

    #------INPUT CLASS---------------------------------------------------------------------------------------------
    # The class CSV_Loader loads files with CSV format. If we want to use other input files with diferent format,
    # we should create a new class inherited from the base class LogsLoader
    input_load = CSV_Loader(input_path)

    #------OPERATION CLASSES---------------------------------------------------------------------------------------
    # Operations. Operation and input classes are link throughout aggregation relationship
    if params.most_frequent is not False:
        operation = MostFrequentIP(input_load)

    elif params.least_frequent is not False:
        operation = LeastFrequentIP(input_load)

    elif params.events_second is not False:
        operation = EventsperSecond(input_load)

    elif params.total_bytes is not False:
        operation = TotalAmountofBytes(input_load)

    #-----OUTPUT CLASS-----------------------------------------------------------------------------------------
    Json_output_Loader(output_path, operation)


if __name__ == "__main__":
    exit(main())
