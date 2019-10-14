import argparse
import sqlalchemy
from sqlalchemy import *
import json
from datetime import datetime
import pymongo
from pymongo import MongoClient



def ArgumentParsing() :
    try :
        parser = argparse.ArgumentParser(description = '''This program moves data from Sqlite DB to Mongo DB
                                                          and selects moved data from Mongo DB.''')
        parser.add_argument('-path_sqlite', '-sqlite', help = 'Enter path to sqlite database file including file name.')
        parser.add_argument('-mongo_host', '-host', help = 'Enter mongo database host name.')
        parser.add_argument('-mongo_port', '-port', type = int, help = 'Enter mongo database port number.')
        parser.add_argument('-mongo_username', '-username', '-user', help = 'Enter mongo database user name (in case authentification required).')
        parser.add_argument('-mongo_password', '-password', '-pass', help = 'Enter mongo database user password (in case authentification required).')
        parser.add_argument('-mongo_database', '-db', help = 'Enter link to mongo database (in case authentification required).')
        global args
        args = parser.parse_args()
    except :
        print('Incorrect input.')
        raise SystemExit()                          #Exit program in case error, don't run the next functions.



def SqliteConnect() :                               #Connect to sqlite database file to get data to move.
    try :
        global engine
        global conn_sqlite
        engine = sqlalchemy.create_engine('sqlite:///' + args.path_sqlite)
        conn_sqlite = engine.connect()
    except :
        print("Can't connect to sqlite database.")
        raise SystemExit()                          #Exit program in case error, don't run the next functions.



def GetDataFromSqlite() :
    try :
        metadata = MetaData()                       #Metadata to reach tables in in sqlite db.
        project_table = Table('Project', metadata, autoload = True, autoload_with = engine)    #Load table "Project".
        global project_columns
        project_columns = [c.name for c in project_table.columns]                              #Store column names from "Project" table.
        global project_qry_result
        project_qry_result = conn_sqlite.execute(select([project_table])).fetchall()           #Select * from Project and store result.
        tasks_table = Table('Tasks', metadata, autoload = True, autoload_with = engine)        #Load table "Tasks".
        global tasks_columns
        tasks_columns = [c.name for c in tasks_table.columns]                                  #Store column names from "Tasks" table.
        global tasks_qry_result
        tasks_qry_result = conn_sqlite.execute(select([tasks_table])).fetchall()               #Select * from Tasks and store result.
    except :
        print("Can't get data from sqlite database.")
        raise SystemExit()                          #Exit program in case error, don't run the next functions.



def ProjectTableData_Transformation() :             #Transform data from "Project" table to "dictionary" format.
    try :
        project_per_record_dict = dict()            #Dictionary to store simply record from the result.

        global project_data_list
        project_data_list = list()                  #List to store all records from "Project" table in "dictionary" format.

        for record in project_qry_result :
            for column in project_columns :               #For each column
                idx = project_columns.index(column)       #get its index.
                if idx == 2 :                             #For columns contain "date" type - convert value to string - sqlalchemy requires.
                    project_per_record_dict[column] = datetime.strftime(record[idx], '%Y-%m-%d') #And assign value from according column to according "key" in dictionary.
                else :
                    project_per_record_dict[column] = record[idx]
            project_data_list.append(project_per_record_dict)     #Add record to list.
            project_per_record_dict = {}                  #Emptify dictionary before storing next record.
    except :
        print("Can't process data from \"Project\" table.")
        raise SystemExit()                          #Exit program in case error, don't run the next functions.



def TasksTableData_Transformation() :               #Transform data from "Tasks" table to "dictionary" format.
    try :                                           #Logic is the same as for "Project" table.
        tasks_per_record_dict = dict()

        global tasks_data_list
        tasks_data_list = list()

        for record in tasks_qry_result :
            for column in tasks_columns :
                idx = tasks_columns.index(column)
                if idx == 4 or idx == 5 :
                    tasks_per_record_dict[column] = datetime.strftime(record[idx], '%Y-%m-%d')
                else :
                    tasks_per_record_dict[column] = record[idx]
            tasks_data_list.append(tasks_per_record_dict)
            tasks_per_record_dict = {}
    except :
        print("Can't process data from \"Tasks\" table.")
        raise SystemExit()                          #Exit program in case error, don't run the next functions.



def MongoConnect() :                                #Connect to Mongo database.
    try :
        global conn_mongo
        if args.mongo_username and args.mongo_password:
            mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (args.mongo_username, args.mongo_password, args.mongo_host, args.mongo_port, args.mongo_database)
            conn_mongo = MongoClient(mongo_uri)
        else:
            conn_mongo = MongoClient(args.mongo_host, args.mongo_port)
    except :
        print("Can't connect to mongo database.")
        raise SystemExit()                          #Exit program in case error, don't run the next functions.



def DropMongoDB() :                                 #Drop mongo database with name "test" if such exists.
    try :
        if 'test' in conn_mongo.list_database_names() :
            conn_mongo.drop_database('test')
    except :
        print("Can't drop existing mongo database \"test\".")



def InsertDataToMongo() :
    try :
        test_db = conn_mongo['test']                #Create mongo database "test".
        global project_collection
        global tasks_collection
        project_collection = test_db['project']     #Create collections.
        tasks_collection = test_db['tasks']
        project_collection.insert_many(project_data_list)    #Insert data into collections.
        tasks_collection.insert_many(tasks_data_list)
    except :
        print("Can't perform specified operations on mongo database.")
        raise SystemExit()                          #Exit program in case error, don't run the next functions.



def SelectDataFromMongo() :
    try :                                           #Select needed data from mongo database and display result.
        fin_query_result = tasks_collection.find({ "status": "Cancelled" }).distinct('Project')
        for row in fin_query_result :
            print(row)
    except :
        print("Can't get data from mongo database.")



if __name__ == '__main__' :
    ArgumentParsing()
    SqliteConnect()
    GetDataFromSqlite()
    ProjectTableData_Transformation()
    TasksTableData_Transformation()
    MongoConnect()
    DropMongoDB()
    InsertDataToMongo()
    SelectDataFromMongo()
