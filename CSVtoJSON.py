import argparse
import csv
import json



def ArgumentParsing() :
    parser = argparse.ArgumentParser(description = 'This is a progran to convert data from csv file to json.')
    parser.add_argument('-path_csv', '-csv', help = 'Type path to csv file including file name.')
    parser.add_argument('-path_json', '-json', help = 'Type path to json file including file name.')
    global args
    args = parser.parse_args()



def CSVtoJSONprocessing() :
    try :
        with open(args.path_csv, 'r', newline = '') as csv_file :            #Open csv file.
            data = csv.DictReader(csv_file, delimiter = ',')                 #Read content as dict - "column name" : "column value"
            try :
                json_file = open(str(args.path_json), 'w')                   #Create json file. If file exists, it will be overwritten.
                for row in data :
                    row = dict(row)                                          #Convert each record from csv - from DictReader to simple dictionary.
                    for key in row.keys() :
                        if key == 'password' :                               #Column "password" will not be represented in json file.
                            del row[key]
                            break;
                    json.dump(row, json_file, indent = 4)                    #Write to json each record per line, indent for better view.
                    json_file.write('\n')
                json_file.close()
            except :
                print("Can't work with json file. Check the path and file name.")
    except :
        print("Can't work with csv file. Check the path and file name.")



if __name__ == '__main__' :
    ArgumentParsing()
    CSVtoJSONprocessing()
