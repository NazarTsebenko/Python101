import argparse
import csv
import re


def ArgumentParsing() :
    parser = argparse.ArgumentParser(description = 'This is a program to get values from certain column in csv file.')
    parser.add_argument('-path_csv', help = 'Type path to the file including file name.')
    parser.add_argument('-col_name', help = '''Type column name.
                        If column name consists of more than word - combine them using '_' symbol.''')
    global args
    args = parser.parse_args()



def CSVProcessing() :
    col_found = False    #Variable to handle situation when there no column with specified name in the file.
    try :
        with open(args.path_csv, 'r', newline = '') as csv_file :
            data = csv.reader(csv_file, delimiter = ',')           #Column values are separated by comma.
            headers = next(data)                                   #Read column names in the file.
            for header in headers :                                #Look for needed column name.
                if header.lower() == re.sub('_', ' ', args.col_name.lower()) :  #Replace '_' with blank space. Comparing column names. Case independent - user can enter column name not followig case.
                    idx = headers.index(header)                    #Get needed column index.
                    col_found = True                               #Store that needed column found.

            if col_found :                                         #Get all values from column using index.
                for row in data :
                    if row[idx] != '' :
                        print(row[idx])
            else :
                print('No such column in the file.')
    except :
        print("Such path or file doesn't exist. Or not all arguments were specified.")



if __name__ == '__main__' :
    ArgumentParsing()
    CSVProcessing()
