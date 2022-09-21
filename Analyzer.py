from argparse import ArgumentParser
import re


# Base class. It will store common input for any existing loader (other formats)
class LogsLoader(object):
    def __init__(self, data_input):
        self.input = str(data_input)

    def get_input(self):
        return self.input


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

    def csv_decode(self):
        # with open(super()._input, 'r') as file:
        try:
            with open(self.get_input(), 'r') as file:
                line_text = file.readline()
                line_number = 0
                fields_list: list = list()
                while line_text:
                    line_text = file.readline()
                    dissection = re.split('\s\s+', line_text)
                    if len(dissection) < 2:     #There are specific cases in which there is only one space between the first and second field
                        fields_list = line_text.split(' ')
                        self.field_1.append(fields_list[0])
                    else:
                        fields_list = dissection[1].split(' ')
                        self.field_1.append(dissection[0])

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
        except Exception as e:
            print("Error: %s", str(e))

        print("El numero de registros es: ", line_number)


def parse_arguments():

    # Load script arguments.

    parser = ArgumentParser(description='Script to analyze logs for SwissRe')

    parser.add_argument('-i', '--input', help='Path to a plain text which contain logs')
    parser.add_argument('-o', '--output', help='Path to a file to save output in plain text JSON format')

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
        input = params.input
        output = params.output
    else:
        print('Input and Output arguments are mandatories. Please re-introduce them')
        return False

    CSV_Loader(input).csv_decode()

    if params.most_frequent is not False:
        pass

    elif params.least_frequent is not False:
        pass

    elif params.events_second is not False:
        pass

    elif params.total_bytes is not False:
        pass


if __name__ == "__main__":
    exit(main())
