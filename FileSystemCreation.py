import os                  #Library for getting information about OS.
from stat import *         #Library for getting statistical information about OS.
import time                #Library to convert time.

other_dir = True           #Variable to make program work repetible.



def FileSystemCreation() : #Function to check whether directory and file exist and create if not.
    is_directory = os.path.isdir(fpath)

    if is_directory :
        print('Such directory already exists.')
    else :
        try :
            os.makedirs(fpath)
            print('Directory ' + fpath + ' was created.')
        except :
            print("You can't create that directory.")

    is_file = os.path.isfile(fpath + '\\' + fname)       #Check if there is such file in given directory.

    if is_file :
        print('Such file already exists.')
        print('')
    else :
        try :
            fcreate = open(fpath + '\\' + fname, 'w')    #Create file in given directory (if doesn't exist.)
            print('File ' + fname + ' was created.')
            print('')
        except :
            print("You can't create that file.")
            print('')



def FileSystemInformation() : #Function to get list of elements in given directory and some statistical information about them.
    try :
        file_list = os.listdir(fpath)                                      #Get list of elements in given directory.

        print('Information about ' + fpath)
        print('')

        for file in file_list :
            stat = os.stat(fpath + '\\' + file)                            #Get statistical information about each element.
            print('Element name: ' + file)
            print('Element size: ' + str(stat[ST_SIZE]) + ' bytes')        #Print element size.
            print('Last modified: ' + str(time.ctime(stat[ST_MTIME])))     #Print last modified time after converting.
            print('-------------------------------------------------')
    except :
        print("You can't access data in such directory. Perhaps that directory doesn't exist.")



if __name__ == '__main__' :      #Main function
    while other_dir :
        print('')
        fpath = input('Please enter a path / directory name: ')
        fname = input('Please enter a file name: ')
        print('')
        FileSystemCreation()
        FileSystemInformation()       #User can create one more directory and file or get information about if wants.
        other_dir = input('Do you want to create (or get information about) other directory and file? (y/n) ').lower() == 'y'
