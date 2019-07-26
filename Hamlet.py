import re                   #Library for using regular expressions.

file_name = "Book.txt"
text = open(file_name, "r") #Read text directly from file.

every_row = []              #Array with type list to store words per each row in text.
words = {}                  #Array with type dictionary to store unique words and their counts.

for line in text :
    every_row = line.strip('\W').lower()                 #Trim row from text on both sides (also cropping any symbol different from
                                                         #letter at the begin and at the end of the row) and result all words in lower case.
    every_row = re.split('\W+\s+|\s+\W+|\s+', every_row) #Separate each word from another using as delimiter: combination of
                                                         #any number of any symbols different from letter and any number of
                                                         #blank spaces; or combination of any number of blank spaces and any
                                                         #number of any symbols different from letter; or any number of blank spaces.
                                                         #Symbols inside words are not delimiters, so such as "we'll", "you're" etc.
                                                         #are counting as one word.
    for word in every_row :
        if word == '' :                                  #There may come empty values from rows. We skip them and don't add to the dictionary.
            continue;
        words[word] = words.get(word, 0) + 1             #Check if the word already exists in the dictionary: if no - add to the dictionary
                                                         #with count 1; if yes - increase count by 1.

text.close()

result = open("Words and counts.txt", "w")               #The result is written to the file.

for key, value in words.items() :
    count = str(key) + ' ' + str(value) + '\n'           #Every word and its count is written on a new line.
    result.write(count)

result.close()
