"""
Problem Set 2, hangman.py.

Name: Nazar Latko
Collaborators: Artem Latko

"""

import random
import string
import os
import sys
import logging
import json

WORDLIST_FILENAME = "words.txt"
JSON_FILENAME = "config.json"

# Determine the path to the current script file
# current_dir: string
current_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script directory
os.chdir(current_dir)

# The path to the configuration file
config_path = os.path.join(current_dir, JSON_FILENAME)

# The path to the text file
text_path = os.path.join(current_dir, WORDLIST_FILENAME)

# We read the configuration file
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

log_level_str = config.get('log_level')

log_level = getattr(logging, log_level_str, logging.DEBUG)

# We set the log format
logging.basicConfig(
    filename=config.get('log_file', 'hangman.log'),
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding="utf-8"
)

if not os.path.exists(text_path):
    logging.critical('File words.txt not found')
    sys.exit("The 'words.txt' file is not found.")


def load_words():
    """
    Return a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    Wordlist (list): list of words (strings).

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code
# -----------------------------------
# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are lowercase.

    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """
    # For each letter in secret_word check if there is any matches.
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing.

    letters_guessed: list (of letters), which letters have been guessed so far
            returns: string, comprised of letters, underscores (_), and spaces that represents
    which letters in secret_word have been guessed so far.
    """
    # Previously set the value of the word to have it changed depending on the guessed letters
    guessed_word = ""
    for letter in secret_word:
        if letter not in letters_guessed:
            letter = "_ "
        guessed_word += letter
    return guessed_word


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far.

    returns: string (of letters), comprised of letters that represents which letters have not
    yet been guessed.
    """
    # Create alphabet
    alphabet = string.ascii_lowercase

    # Remove guessed letters from the alphabet
    for letter in letters_guessed:
        alphabet = alphabet.replace(letter, '')
    return alphabet


def if_incorrect_input(warnings_remaining, guesses_remaining, letters_guessed):
    """
    Process invalid input.

    warnings_remaining: int, how many warnigs left player has.
    guesses_remaining: int, how many guesses left player has.
    letters_guessed: list (of letters), which letters have been guessed so far.
    If there was an error while inputting, we decrease by 1 user's warning
    and if it reaches 0 we decreases user's attempts by 1
    returns: int, int, how many warnings and guesses left after invalid input
    """
    if warnings_remaining > 0:
        warnings_remaining -= 1
        logging.error("Error while input!")
        print(f'''Oops! That is not a valid letter. You have {warnings_remaining} warnings left: {get_guessed_word(secret_word, letters_guessed)}''')
        print("---------------")
    else:
        print(f"Oops! That is not a valid letter. You have no warnings left: {get_guessed_word(secret_word, letters_guessed)}")
        print("---------------")
        logging.error("Error while input!")
        guesses_remaining -= 1
    return warnings_remaining, guesses_remaining


def if_already_guessed(warnings_remaining, guesses_remaining, letters_guessed):
    """
    Process repeating input.

    warnings_remaining: int, how many warnigs left player has.
    guesses_remaining: int, how many guesses left player has.
    letters_guessed: list (of letters), which letters have been guessed so far.
    If there was repeating input, we decrease by 1 user's warning
    and if it reaches 0 we decreases user's attempts by 1
    returns: int, int, how many warnings and guesses left after invalid input
    """
    warnings_remaining = int(warnings_remaining)
    guesses_remaining = int(guesses_remaining)
    if warnings_remaining > 0:
        warnings_remaining -= 1
        print(f'''Oops! You've already guessed that letter. You have {warnings_remaining} warnings left: {get_guessed_word(secret_word, letters_guessed)}''')
        print("---------------")
        logging.error("Already guessed that letter")
    else:
        print(f'''Oops! You've already guessed that letter. You have no warnings left: {get_guessed_word(secret_word, letters_guessed)}''')
        print("---------------")
        logging.error("Already guessed that letter")
        guesses_remaining -= 1
    return warnings_remaining, guesses_remaining


def hangman(secret_word):
    
    loud_sounds = "aeiou"
    guesses_remaining = 6
    warnings_remaining = 3

    # len_of_word: integer
    len_of_word = len(secret_word)

    # Create list to append guessed letters
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len_of_word} letters long")

    while guesses_remaining > 0:
        print(f"You have {guesses_remaining} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        user_input = input("Please guess a letter: ").lower()       # Translate to the lower case to operate the letter user input
        logging.debug(f"User's input: {user_input}")

        # Check if user's input is letter and have lenght equal 1
        if len(user_input) == 1 and user_input.isalpha():

            # Check if the letter in secret word and if it is included
            # then add to the list with guessed letters
            if user_input in secret_word:
                if user_input not in letters_guessed:
                    letters_guessed.append(user_input)
                    print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
                    print("---------------")
                    logging.info("Good guess")

                # If user entered the same symbol for the second time, we decrease by 1 user's warning
                # and if it reaches 0 we decreases user's attempts by 1
                else:
                    warnings_remaining, guesses_remaining = if_already_guessed(warnings_remaining, guesses_remaining, letters_guessed)
                if is_word_guessed(secret_word, letters_guessed) is True:
                    total_score = guesses_remaining * len(letters_guessed)   # Calculate the score user will get
                    print(f"Congratulations, you won! Your total score for this game is: {total_score}")
                    logging.info("Victory")
                    break
            else:
                if user_input not in letters_guessed:
                    print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")
                    print("---------------")
                    logging.info("Bad guess")
                    letters_guessed.append(user_input)
                    if user_input in loud_sounds:
                        guesses_remaining -= 2
                    else:
                        guesses_remaining -= 1

                # If user entered the same symbol for the second time, we decrease by 1 user's warning
                # and if it reaches 0 we decreases user's attempts by 1
                else:
                    warnings_remaining, guesses_remaining = if_already_guessed(warnings_remaining, guesses_remaining, letters_guessed)
        else:
            # If there was an error while inputting, we decrease by 1 user's warning
            # and if it reaches 0 we decreases user's attempts by 1
            warnings_remaining, guesses_remaining = if_incorrect_input(warnings_remaining, guesses_remaining, letters_guessed)
    if guesses_remaining <= 0:
        print(f"Sorry, you ran out of guesses. The word was {secret_word}")
        logging.info("Defeat")



def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word.

    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
    corresponding letters of other_word, or the letter is the special symbol _ ,
    and my_word and other_word are of the same length;
    False otherwise:
    """
    # Delete spaces
    my_word = str(my_word).replace(" ", "")
    if len(my_word) == len(other_word):
        for n in range(len(my_word)):
            if my_word[n] == "_":
                continue
            else:
                if my_word[n] == other_word[n]:
                    continue
                else:
                    return False
    else:
        return False
    return True


def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word.

    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.
    """
    similar_words = []
    for word in wordlist:
        if match_with_gaps(my_word, word) is True:
            similar_words.append(word)
        else:
            continue
    return similar_words


def hangman_with_hints(secret_word, hints_on=True):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.
    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.
    * The user should start with 6 guesses
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.
    * After each guess, you should display to the user the
      partially guessed word so far.
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.
    Follows the other limitations detailed in the problem write-up.
    """
    loud_sounds = "aeiou"
    guesses_remaining = 6
    warnings_remaining = 3
    show_hints = "*"

    # len_of_word: integer
    len_of_word = len(secret_word)

    # Create list to append guessed letters
    letters_guessed = []
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len_of_word} letters long")

    while guesses_remaining > 0:
        print(f"You have {guesses_remaining} guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        user_input = input("Please guess a letter: ").lower()       # Translate to the lower case to operate the letter user input
        logging.debug(f"User's input: {user_input}")

        # Check if user's input is letter and have lenght equal 1
        if len(user_input) == 1 and user_input.isalpha():

            # Check if the letter in secret word and if it is included
            # then add to the list with guessed letters
            if user_input in secret_word:
                if user_input not in letters_guessed:
                    letters_guessed.append(user_input)
                    print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
                    print("---------------")
                    logging.info("Good guess")

                # If user entered the same symbol for the second time, we decrease by 1 user's warning
                # and if it reaches 0 we decreases user's attempts by 1
                else:
                    warnings_remaining, guesses_remaining = if_already_guessed(warnings_remaining, guesses_remaining, letters_guessed)
                if is_word_guessed(secret_word, letters_guessed) is True:
                    total_score = guesses_remaining * len(letters_guessed)   # Calculate the score user will get
                    print(f"Congratulations, you won! Your total score for this game is: {total_score}")
                    logging.info("Victory")
                    break
            else:
                if user_input not in letters_guessed:
                    letters_guessed.append(user_input)
                    print(f"Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}")
                    print("---------------")
                    logging.info("Bad guess")
                    if user_input in loud_sounds:
                        guesses_remaining -= 2
                    else:
                        guesses_remaining -= 1

                # If user entered the same symbol for the second time, we decrease by 1 user's warning
                # and if it reaches 0 we decreases user's attempts by 1
                else:
                    warnings_remaining, guesses_remaining = if_already_guessed(warnings_remaining, guesses_remaining, letters_guessed)
        else:
            if user_input == show_hints and hints_on is True:
                print("Possible word matches are: ", end="")
                print(*show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
                print("---------------")
                logging.info("Shows possible matches")
            else:
                # If there was an error while inputting, we decrease by 1 user's warning
                # and if it reaches 0 we decreases user's attempts by 1
                warnings_remaining, guesses_remaining = if_incorrect_input(warnings_remaining, guesses_remaining, letters_guessed)
    if guesses_remaining <= 0:
        print(f"Sorry, you ran out of guesses. The word was {secret_word}")
        logging.info("Defeat")



if __name__ == "__main__":
    logging.info("Program started")
    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

    ###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word, hints_on=True)
    logging.info("Program ended")
