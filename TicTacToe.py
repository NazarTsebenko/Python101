import random                                          #Import library for random choice of number.

gameboard = range(1, 10)                               #Variable for futher gameboard creation.
cells = list()                                         #List to store actual situation on the gameboard. It is updated during each turn.

print("-------------")                                 #Gameboard visualition and create initial condition on it.
for i in range(3) :
    cells.append(gameboard[0+i*3])
    cells.append(gameboard[1+i*3])
    cells.append(gameboard[2+i*3])
    print("|", gameboard[0+i*3], "|", gameboard[1+i*3], "|", gameboard[2+i*3], "|")
    print("-------------")

is_winner = False
turns = 9
user_turn = random.choice([True, False])                #Random choise to define who goes first.

if user_turn == True :
    print("")
    print('You go first.')
else :
    print("")
    print('CPU goes first.')

while is_winner == False and turns != 0 :               #Game continues until winner appears or there will not be turns.
    if user_turn == False :                             #Here begins code for CPU turn.
        print("")
        print('CPU goes.')
        print("")
        cells_for_cpu = []                              #List of available cells on the gameboard, for CPU. List is regenerated each time CPU goes.
        for cell in cells :
            if isinstance(cell, int) == True :
                cells_for_cpu.append(cell)              #Filling the list with available cells. Leave only digits. Exclude letters (X, O).
        digit_cpu = random.choice(cells_for_cpu)        #CPU chooses random number.
        for cell in cells :                             #Update situation on the gameboard.
            if cell == digit_cpu :
                idx = cells.index(digit_cpu)
                cells[idx] = 'O'
                print("-------------")                  #Visualize gameboard with actual situation.
                for i in range(3) :
                    print("|", cells[i*3], "|", cells[1+i*3], "|", cells[2+i*3], "|")
                    print("-------------")
                                                                    #Check whether there is a winner.
                if (cells[0] == cells[1] == cells[2] == 'O') or \
                   (cells[3] == cells[4] == cells[5] == 'O') or \
                   (cells[6] == cells[7] == cells[8] == 'O') or \
                   (cells[0] == cells[3] == cells[6] == 'O') or \
                   (cells[1] == cells[4] == cells[7] == 'O') or \
                   (cells[2] == cells[5] == cells[8] == 'O') or \
                   (cells[0] == cells[4] == cells[8] == 'O') or \
                   (cells[2] == cells[4] == cells[6] == 'O') :
                    is_winner = True
                    print('CPU won.')
                else :
                    turns = turns - 1
                    user_turn = True                     #Pass a turn to a user.
    else :
        turn_done = False                                #Here begins code for user turn.
        try :                                            #Handle situation when user enters non-appropriate value, letter or symbol instead of digit.
            print("")
            digit = int(input('Your turn: '))
        except :
            print('You must enter only an integer of the available on the gameboard.')
            continue;
        for cell in cells :                              #Update situation on the gameboard.
            if cell == digit :
                idx = cells.index(digit)
                cells[idx] = 'X'
                print("-------------")                   #Visualize gameboard with actual situation.
                for i in range(3) :
                    print("|", cells[i*3], "|", cells[1+i*3], "|", cells[2+i*3], "|")
                    print("-------------")
                                                                    #Check whether there is a winner.
                if (cells[0] == cells[1] == cells[2] == 'X') or \
                   (cells[3] == cells[4] == cells[5] == 'X') or \
                   (cells[6] == cells[7] == cells[8] == 'X') or \
                   (cells[0] == cells[3] == cells[6] == 'X') or \
                   (cells[1] == cells[4] == cells[7] == 'X') or \
                   (cells[2] == cells[5] == cells[8] == 'X') or \
                   (cells[0] == cells[4] == cells[8] == 'X') or \
                   (cells[2] == cells[4] == cells[6] == 'X') :
                    turn_done = True
                    is_winner = True
                    print('You won.')
                else :
                    turn_done = True
                    turns = turns - 1                    #Count turns left to handle situation when draw occurs.
                    user_turn = False                    #Pass a turn to CPU.
        if turn_done == False :                          #Handle situation when user enters a digit but not from the list of available.
            print('You must enter only an integer of the available on the gameboard.')

if turns == 0 :                                          #Check whether draw occurred.
    print('Draw.')
