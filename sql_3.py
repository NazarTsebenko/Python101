import argparse
import os
import sqlite3
import csv



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

        global conn
        global cur
        conn = sqlite3.connect(args.path_database)  #Create DB.
        cur = conn.cursor()                         #Create cursor.

        #Create tables.
        cur.executescript('''create table Project (Name TEXT NOT NULL PRIMARY KEY,
                                                   description TEXT,
                                                   deadline DATE)''')

        cur.executescript('''create table Tasks (id INTEGER NOT NULL PRIMARY KEY UNIQUE,
                                                 priority INTEGER,
                                                 details TEXT,
                                                 status TEXT,
                                                 deadline DATE,
                                                 completed DATE,
                                                 Project TEXT,
                                                 FOREIGN KEY(Project) REFERENCES Project(Name))''')
    except :
        print("Can't create DB or connect to it.")
        raise SystemExit()                          #Exit program in case error, don't run the next functions.



def CSVtoDBprocessing() :
    try :
        with open(args.path_csv, 'r', newline = '') as csv_file :     #Read data from csv and store it in dictionary (column: value).
            data = csv.DictReader(csv_file, delimiter = ',')
            for row in data :
                row = dict(row)

                #Check whether project with given name already inserted into table.
                cur.execute('select Name from Project where Name = ?', (row['project_name'],))
                result = cur.fetchone()

                #Insert record if it has not been inserted yet.
                if result is None :
                    cur.execute('insert into Project (Name, description, deadline) values (?, ?, ?)',
                    (row['project_name'], row['project_description'], row['project_deadline'],))


                #Check whether task with given id already inserted into table.
                cur.execute('select id from Tasks where id = ?', (row['task_id'],))
                result = cur.fetchone()

                #Insert record if it has not been inserted yet.
                if result is None :
                    cur.execute('''insert into Tasks (id, priority, details, status, deadline, completed, Project)
                                              values (?, ?, ?, ?, ?, ?, ?)''',
                    (row['task_id'], row['task_priority'], row['task_details'], row['task_status'], row['task_deadline'],
                    row['task_completed'], row['project_name'],))

        conn.commit()                               #Commit transaction.
    except :
        print("Can't work with csv file or failed to insert data.")
        raise SystemExit()                          #Exit program in case error, don't run the next functions.



def SelectProject() :
    try :
        if args.project_name is not None :          #Handle case when user didn't specify project name.
            #Select from "Tasks" table.
            cur.execute('select * from Tasks where Project = ?', (args.project_name,))
            qry_result = cur.fetchall()

            #Print result per record returned.
            for record in qry_result :
                print(record)
        else :
            print('Project name was not specified.')

        cur.close()                                 #Close cursor.
    except :
        print("Can't select data.")



if __name__ == '__main__' :
    ArgumentParsing()
    DBcreation()
    CSVtoDBprocessing()
    SelectProject()
