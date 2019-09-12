import argparse
import json
import re



def ArgumentParser() :
    parser = argparse.ArgumentParser(description = 'This is a progran to convert data from sql dump file to json.')
    parser.add_argument('-path_sql_dump', '-sql_dump', '-sql', help = 'Type path to sql dump file including file name.')
    parser.add_argument('-path_json', '-json', help = 'Type path to json file including file name.')
    global args
    args = parser.parse_args()



def SQLDUMPtoJSONprocessing() :
    per_record_dict = {}             #Create dictionary to store values per record with column names.
    idx = 0                          #Create index to determine which column the value is for.

    try :
        with open(args.path_sql_dump, 'r') as sql_dump :
            sql_dump_str = sql_dump.read().lower()             #Read sql file as simple text file.
            sql_dump_str = re.sub('\n', ' ', sql_dump_str)     #Remove \n symbols from text (replace with blank space).
            #Get column names from "insert into..." script.
            columns = re.sub('[^\s\w]', '', str(re.findall(r'\(.+\)', str(re.findall(r'insert into.+values', sql_dump_str))))).split()
            #Get values from "insert into..." script.
            values = re.sub('[^\s\w]', '', str(re.findall(r'\(.+\)', str(re.findall(r'values.+;', sql_dump_str))))).split()
            #Count columns in the table to divide all values into records.
            columns_count = len(columns)
            try :
                json_file = open(str(args.path_json), 'w')      #Create json file. If file exists, it will be overwritten.
                for value in values :
                    if columns[idx] == 'password' :             #Column "password" will not be represented in json file.
                        idx = idx + 1
                        continue;
                    per_record_dict[columns[idx]] = value       #Assign each value to appropriate column using dictionary.
                    idx = idx + 1
                    #All valueas for all records are stored in the list.
                    #For example, if there are 7 columns, we insert 7 values in appropriate columns as one record.
                    #And the next 7 values as the next record and so on.
                    if idx == columns_count :
                        json.dump(per_record_dict, json_file, indent = 4)       #Write current dictionary to json per line, indent for better view.
                        json_file.write('\n')
                        per_record_dict.clear()                                 #Clear dictionary after writing record (record from sql table).
                        idx = 0                                                 #Dictionaty always contains information only about one record. Nullify index to start from the first column again.
                json_file.close()
            except :
                print("Can't work with json file. Check the path and file name.")
    except :
        print("Can't work with sql file. Check the path and file name.")



if __name__ == '__main__' :
    ArgumentParser()
    SQLDUMPtoJSONprocessing()
