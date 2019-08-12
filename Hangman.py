import re

given_word = input('Please give a word to guess: ')                                       #User enters word to guess.
print('')
print('How many letters(symbols) does this word contain?')
print('')
given_word_length = len(given_word)                                                       #Count how many letters are in the word.

print('This word contains ' + str(given_word_length) + ' letters (including symbols).')
print('')

words_base_file = open('hangman_list.txt', "r")                                           #Open list of words in txt file.
words_base_set = set()

for word in words_base_file :
    word = word.strip().lower()                                                           #Cut all words on both sides and result in lowercase.
    if len(word) == given_word_length :
        words_base_set.add(word)                                                          #Add to collection only words with needed length.

words_base_file.close()

user_answer = 1
attempt_count = 0

while True :                                                                              #Game ended when CPU guessed the word or word not in the file.
    if int(user_answer) == 1 :
        word_in_progress = input('Open the letter: ')                                     #User opens a letter at the beggining and each time when CPU guessed.
        print('')                                                                         #Shouls type in format __m_ (home).
    else :
        word_in_progress = word_in_progress                                               #Branch if CPU didn't guess the letter. CPU is going to try again.

    if '_' not in word_in_progress :                                                      #Check whether CPU guessed all letters in the word.
        break;

    pattern = re.sub('_', r'[\\w\\W]', word_in_progress)                                  #Make pattern to find words.

    for word in words_base_set.copy() :                                                   #Find all words matched the pattern and leave only them in set.
        result = re.findall(pattern, word)
        if result == [] :
            words_base_set.remove(word)

    for symbol in word_in_progress :                                                      #Here is the code for simple CPU AI.
        if symbol != '_' :                                                                #CPU tries to guess all letters in the word for as minimum number of attempts as possible.
            start_idx = word_in_progress.index(symbol)                                    #CPU will try to guess the adjacent letter to the already opened letter. On the left side or on the right side.
            break;

    for symbol in word_in_progress[::-1] :
        if symbol != '_' :
            end_idx = given_word_length - (word_in_progress[::-1].index(symbol) + 1)
            break;

    letters_processing_dict = {}                                                          #Create dictionary for storring count of each letter (on current position CPU will investigate).

    if start_idx != 0 :                                                                                            #Check whether there is a letter to guess on the left side.
        cur_idx = start_idx - 1                                                                                    #If so - try.
        for word in words_base_set :
            letters_processing_dict[word[cur_idx]] = letters_processing_dict.get(word[cur_idx], 0) + 1
    elif end_idx != given_word_length - 1 :                                                                        #Or on the right side.
        cur_idx = end_idx + 1
        for word in words_base_set :
            letters_processing_dict[word[cur_idx]] = letters_processing_dict.get(word[cur_idx], 0) + 1
    else :
        for symbol in word_in_progress :                                                                           #Or there is a letter to guess between two already opened letters.
            if symbol == '_' :
                cur_idx = word_in_progress.index(symbol)
                for word in words_base_set :
                    letters_processing_dict[word[cur_idx]] = letters_processing_dict.get(word[cur_idx], 0) + 1
    try :
        max_count_letter = max(letters_processing_dict.values())                                                   #Define the most common letter (on current processing position).
        sum_count_letter = sum(letters_processing_dict.values())                                                   #Define general count of all letters (on current processing position).
    except :
        attempt_count = 0                                                                                          #Handle situation when user entered the word which is absent in txt file.
        break;

    for key, value in letters_processing_dict.items() :
        if value == max_count_letter :
            print("With probability " + str(round((max_count_letter/sum_count_letter)*100, 2)) + "% this is the letter '" + key + "'.")       #Calculate the probability that CPU will guess the letter this time.
            print('')
            attempt_count = attempt_count + 1                                                                                                 #Count attempts CPU makes.
            break;

    user_answer = input("Please enter '1' - if yes, '0' - if not: ")                                                #User defines whether CPU guessed the letter or not.
    print('')

    if int(user_answer) != 1 :                                                                                      #If CPU didn't guess a letter - rebuild pattern and remove all words matched pattern from set.
        cpu_fault = word_in_progress
        cpu_fault = cpu_fault[:cur_idx] + cpu_fault[cur_idx].replace('_', key) + cpu_fault[cur_idx+1:]
        pattern = re.sub('_', r'[\\w\\W]', cpu_fault)
        for word in words_base_set.copy() :
            result = re.findall(pattern, word)
            if result :
                words_base_set.remove(word)

if attempt_count != 0 :
    print('CPU guessed the word within ' + str(attempt_count) + ' attempts.')                                       #CPU guessed all letters in the word. Print result.
else :
    print('Given word is absent in CPU database.')                                                                  #Handle situation when user entered the word which is absent in txt file.
