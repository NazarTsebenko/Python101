import re
from functools import reduce
from itertools import chain
from collections import Counter
import typing


def set_words(word_len: int, filename: str = "hangman_list.txt") -> typing.Set[str]:  #Set the proper file name.
    with open(filename) as word_file:
        return {
            word.lower()
            for word in map(str.strip, word_file.readlines())
            if len(word) == word_len and word.isalpha()
        }


def find_words(guesses: str, current_word: str, all_words: typing.Iterable) -> typing.List[str]:
    substitute: str = '.' if len(guesses) == 0 else f"[^{guesses}]"
    # Представляет текущее слово в качестве регулярного выражения
    current_word_regex: typing.Pattern = re.compile(current_word.replace('_', substitute))
    return [word for word in all_words if current_word_regex.match(word)]


def count_letters(possible_words: typing.Iterable) -> Counter:
    return Counter(chain.from_iterable(possible_words))


def get_percent(stats: Counter) -> typing.Tuple[str, float]:

    likeliest_letter, count = stats.most_common(1)[0]
    likelihood = count / sum(stats.values()) * 100.0
    return likeliest_letter, likelihood


def antycheat(user_input: str, last_user_input: str, initial_len_of_input: int) -> typing.Tuple[str, int]:

    if initial_len_of_input == -1:
        return user_input, len(user_input)

    corrected_input: str = user_input

    while len(corrected_input) != initial_len_of_input:
        print("Ты жульничаешь? Вроде в прошлый раз слово было другой длины")
        print(f"У меня все ходы записаны. Последний вариант был таким {last_user_input} и букв там было {len(last_user_input)}.")
        corrected_input = input("Попробуй еще раз ").lower()

    differences: typing.List[bool] = [last_user_input[i] != corrected_input[i]
                                      for i in range(initial_len_of_input)
                                      if last_user_input[i] != '_']

    if len(differences) == 0:
        return corrected_input, initial_len_of_input

    has_differences: bool = all(differences) or reduce(lambda x, y: x != y, differences)

    while has_differences:
        print("Что-то тут не так.")
        print("В прошлый раз буквы были на других местах.")
        print(f"А именно {last_user_input}.")
        corrected_input = input("Давай, соберись. Попробуй снова   ").lower()

        differences = [last_user_input[i] != corrected_input[i]
                       for i in range(initial_len_of_input)
                       if last_user_input[i] != '_']
        has_differences = all(differences) or reduce(lambda x, y: x != y, differences)

    return corrected_input, initial_len_of_input

#Function to handle empty input or input with inappropriate symbols from user at the beginning of game.
def handle_wrong_initial_input(current_word: str):

    while len(current_word) == 0:
        current_word = input("Ти не загадав слово. Спробуй ще раз: ")

    while re.findall('[^_]', current_word):     #Only '_' is allowed at the beginning of game.
        current_word = input("Потрiбно вводити тiльки _ . Спробуй ще раз: ")

    return current_word

#Function to handle input with inappropriate symbols or digits from user.
def handle_wrong_symbols_input(current_word: str):

    while len(current_word) == 0:
        current_word = input("Ти не загадав слово. Спробуй ще раз: ")

    while re.findall('[^_A-Za-z]', current_word):     #Only '_' and letters are allowed at theese steps.
        current_word = input("Потрiбно вводити тiльки _ i/або букви . Спробуй ще раз: ")

    return current_word

def play_game():
#Инициализируем все перед началом игры
    is_playing: bool = True
    was_correct: bool = False      #Fixed bug

    guesses: str = ""
    current_word = input("Загадай, будь ласка, слово. Введи стiльки _ скiльки букв у словi: ")   #Fixed bug. Added logic to start game in proper way.
    current_word = handle_wrong_initial_input(current_word)      #Handle empty input from user at the beginning of game.
    len_of_word = len(current_word)
    last_word = current_word                #Added logic to write initial pattern to antycheat.
    current_word, len_of_word = antycheat(current_word, last_word, len_of_word)

    words: typing.Set[str] = set()

    while is_playing:
        if was_correct:
            last_word: str = current_word
            print(" Помнишь какое слово ты загадал ?")
            current_word = input("(Введи, пожалуйста, угаданные мной буквы, а остальные замени _ ) ").lower()
            current_word = handle_wrong_symbols_input(current_word)
            current_word, len_of_word = antycheat(current_word, last_word, len_of_word)

        # если счетчик неугаданных букв равен нулю то конец игры
        if current_word.count('_') == 0:
            break

        # подсчет неудачных попыток
        guesses += ''.join([guess for guess in current_word if guess != '_' and guess not in guesses])

        if len(words) == 0:
            words = set_words(len(current_word))

        possible_words: typing.List[str] = find_words(guesses, current_word, words)

        print(f"Выбираем из {len(possible_words)} подходящих слов")

        #Handle case when given word is absent in words database. In case no words left.
        if len(possible_words) == 0:
            print("Очевидно, я не знаю такого слова. Здаюсь.")
            break

        if len(possible_words) <= 10:
            [print(word) for word in possible_words]

        if len(possible_words) == 1:
            print(f"Очевидно это слово {possible_words[0]}.")
            was_correct = input(f"Tak? (y/n) ").lower() == 'y' #One word left. User should commit it == given word.
            if was_correct:
                print(f"Это было не сложно, мне понадобилось всего {len(guesses)} попыток!")
            else:      #Handle case when given word is absent in words database. In case one word left but it != given word.
                print("Очевидно, я не знаю такого слова. Здаюсь.")
            break

        stats_temp: Counter = count_letters(possible_words)

        stats: Counter = Counter({key: value for key, value in stats_temp.items() if key not in guesses})

        print("Скорее всего это буква...")
        likeliest_letter: typing.Tuple[str, float] = get_percent(stats)
        print(f"{likeliest_letter[0]} с вероятностью {likeliest_letter[1]:.2f}%")

        was_correct = input("Я конечно прав? (y/n) ").lower() == 'y'

        guesses += likeliest_letter[0]

        print("")

    #Fixed bug. Successful message only if CPU guesses the word.
    if len(possible_words) != 1 and len(possible_words) != 0:
        print(f"Это было не сложно, мне понадобилось всего {len(guesses)} попыток!")

if __name__ == '__main__':
    play_again: bool = True
    while play_again:
        play_game()
        play_again = input("Мне понравилось. Сыграем еще раз? (y/n) ").lower() == 'y'
    print("")
