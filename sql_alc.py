import argparse
import os
import sqlalchemy
from sqlalchemy import *        #To use class MetaData.
import csv
from datetime import datetime   #To convert string to date and vice versa.



def ArgumentParsing() :
    try :
        parser = argparse.ArgumentParser(description = '''This program creates DB, inserts data from csv file
                                                          and selects inserted data.''')
        parser.add_argument('-path_database', '-database', '-db', help = 'Type path to database file including file name.')
        parser.add_argument('-path_csv', '-csv', help = 'Type path to csv file including file name.')
        parser.add_argument('-project_name', '-project', '-prj', help = 'Specify project name to select information about.')
        global args
        args = parser.parse_args()
    except :
        print('Incorrect input.')
        raise SystemExit()                          #Exit program in case error, don't run the next functions.



def DBcreation() :
    try :
        if os.path.exists(args.path_database) :     #Delete DB file if exists.
            os.remove(args.path_database)

        #Create DB and tables.
        global engine
        engine = sqlalchemy.create_engine('sqlite:///' + args.path_database)
        metadata = MetaData()

        global project
        project = Table('Project', metadata,
            Column('Name', Text, nullable = False, primary_key = True),
            Column('description', Text),
            Column('deadline', Date)
        )

        global tasks
        tasks = Table('Tasks', metadata,
            Column('id', Integer, nullable = False, primary_key = True, unique = True),
            Column('priority', Integer),
            Column('details', Text),
            Column('status', Text),
            Column('deadline', Date),
            Column('completed', Date),
            Column('Project', Text, ForeignKey('Project.Name'))
        )

        metadata.create_all(engine)                 #Finish DB creation.
    except :
        print("Can't create DB.")
        raise SystemExit()                          #Exit program in case error, don't run the next functions.



def CSVtoDBprocessing() :
    try :
        global conn
        conn = engine.connect()                     #Connect to DB.

        #Read data from csv and store it in dictionary (column: value).
        with open(args.path_csv, 'r', newline = '') as csv_file :
            data = csv.DictReader(csv_file, delimiter = ',')
            for row in data :
                row = dict(row)

                #If some date in csv file is empty - replace it with default value: 0001-01-01.
                if row['project_deadline'] == '' :
                    row['project_deadline'] = '0001-01-01'

                if row['task_deadline'] == '' :
                    row['task_deadline'] = '0001-01-01'

                if row['task_completed'] == '' :
                    row['task_completed'] = '0001-01-01'

                #Check whether project with given name already inserted into table.
                result = conn.execute(select([project]).where(project.c.Name == row['project_name'])).fetchone()
                #Insert record if it has not been inserted yet.
                if result is None :
                    conn.execute(project.insert(), [
                    {'Name': row['project_name'], 'description': row['project_description'],      #While inserting it is needed to conver date
                    'deadline': datetime.strptime(row['project_deadline'], '%Y-%m-%d').date()}    #written in csv as string to date type.
                    ])

                #Check whether task with given id already inserted into table.
                result = conn.execute(select([tasks]).where(tasks.c.id == row['task_id'])).fetchone()
                #Insert record if it has not been inserted yet.
                if result is None :
                    conn.execute(tasks.insert(), [
                    {'id': row['task_id'], 'priority': row['task_priority'], 'details': row['task_details'],
                    'status': row['task_status'], 'deadline': datetime.strptime(row['task_deadline'], '%Y-%m-%d').date(),
                    'completed': datetime.strptime(row['task_completed'], '%Y-%m-%d').date(), 'Project': row['project_name']}
                    ])
    except :
        print("Can't work with csv file or failed to insert data.")
        raise SystemExit()                          #Exit program in case error, don't run the next functions.



def SelectProject() :
    try :
        if args.project_name is not None :          #Handle case when user didn't specify project name.
            #Select from "Tasks" table.
            qry_result = conn.execute(select([tasks]).where(tasks.c.Project == args.project_name)).fetchall()

            #Print result per record returned.
            for record in qry_result :
                record = list(record)
                record[4] = datetime.strftime(record[4], '%Y-%m-%d')    #To display result in appropriate way it is needed
                record[5] = datetime.strftime(record[5], '%Y-%m-%d')    #to convert date from DB back to string format.
                print(record)
        else :
            print('Project name was not specified.')
    except :
        print("Can't select data.")



if __name__ == '__main__' :
    ArgumentParsing()
    DBcreation()
    CSVtoDBprocessing()
    SelectProject()
