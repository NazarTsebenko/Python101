import os                  #Library for getting information about OS.

other_dir = True           #Variable to make program work repetible.

def FileSystemCheck() :    #Function to check whether directory and file exist.
    fpath = input('Please enter a path / directory name: ')
    fname = input('Please enter a file name: ')

    is_directory = os.path.isdir(fpath)
    is_file = os.path.isfile(fpath + '\\' + fname)   #Check if there is such file in given directory.

    if is_directory :
        print('Such directory exists: "' + fpath + '".')
    else :
        print('There is no such directory: "' + fpath + '".')

    if is_file :
        print('Such file exists: "' + fname + '".')
    else :
        print('There is no such file: "' + fname + '".')

if __name__ == '__main__' :  #Main function.
    while other_dir :
        FileSystemCheck()    #User can check one more directory and file if wants.
        other_dir = input('Do you want to check other directory and file? (y/n) ').lower() == 'y'
