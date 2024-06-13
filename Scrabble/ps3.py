import math
import random
import os
import json
import logging
import sys

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
WILDCARD = "*"
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1,
    'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
    's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

WORDLIST_FILENAME = "words.txt"
JSON_FILENAME = "config.json"

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
    filename=config.get('log_file', 'ps3.log'),
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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    logging.info("Words were loaded")
    return wordlist


def get_frequency_dict(sequence):
    """
    Return a dictionary from sequence.

    The keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq
#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Return the score for a word. Assume the word is a valid word.

    You may assume that the input word is always either a string of letters,
    or the empty string "". You may not assume that the string will only contain
    lowercase letters, so you will have to handle uppercase and mixed case strings
    appropriately.
    The score for a word is the product of two components:
    The first component is the sum of the points for letters in the word.
    The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played
    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word_length = len(word)
    sum_of_points = 0
    for letter in word:
        letter = letter.lower()
        sum_of_points += SCRABBLE_LETTER_VALUES[letter]
    second_component = max(1, 7 * word_length - 3 * (n - word_length))
    word_score = sum_of_points*second_component
    logging.info("Word score was calculated")
    return word_score


def display_hand(hand):
    """
    Display the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')    
    print()                             




def deal_hand(n):
    """
    Return a random hand containing n lowercase letters.

    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand = {}
    num_vowels = int(math.ceil(n / 3))
    hand["*"] = 1
    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    logging.info("Hand dictionary was created successfully")
    return hand


def update_hand(hand, word):
    """
    Create new updated hand.

    Do NOT assume that hand contains every letter in word at least as many times as the letter appears in word.
    Letters in word that don't appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the count in the returned hand to 0
    (or remove the letter from the dictionary, depending on how your code is structured).

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
    word = word.lower()
    new_hand = hand.copy()
    for letter in word:
        if letter in new_hand:
            new_hand[letter] -= 1
            if new_hand[letter] == 0:
                del new_hand[letter]
    logging.info("Hand was updated succesfully")
    return new_hand




def is_valid_word(word, hand, word_list):
    """
    Return bool value dependind on wether valid word.

    Return True if word is in the word_list and is entirely composed of letters in the hand.
    Otherwise, returns False. Does not mutate hand or word_list.
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word = word.lower()
    if word in word_list:
        for letter in word:
            if letter in hand and hand[letter] >= word.count(letter):
                continue
            else:
                logging.info("Invalid word")
                return False
        logging.info("Valid word")
        return True
    else:
        wildcard_index = word.find(WILDCARD)
        if wildcard_index != -1:
            for vovel in VOWELS:
                new_word = word[0: wildcard_index] + vovel + word[wildcard_index + 1:]
                if new_word in word_list:
                    logging.info("Valid word")
                    return True
            logging.info("Invalid word")
            return False
        else:
            logging.info("Invalid word")
            return False




def calculate_handlen(hand):
    """
    Return the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """
    handlen = 0
    for letter in hand:
        handlen += hand[letter]
    logging.info("Handlen was succesfully calculated")
    return handlen


def play_hand(hand, word_list):
    """
    Play hand.

    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
    """
    total_score = 0
    while calculate_handlen(hand) > 0:
        print("Current hand: ", end='')
        display_hand(hand)
        user_input = input("Enter word, or “!!” to indicate that you are finished: ")
        logging.debug(f"User's input: {user_input}")
        if user_input == "!!":
            break
        else:
            if is_valid_word(user_input, hand, word_list) is True:
                word_score = get_word_score(user_input, calculate_handlen(hand)-len(user_input))
                total_score += word_score
                print(f'"{user_input}"" earned {word_score} points. Total: {total_score} points')
            else:
                print("This is not a valid word. Please choose another word.")
            hand = update_hand(hand, user_input)
        print()
    if calculate_handlen(hand) == 0:
        print(f"Ran out of letters. Total score: {total_score}")
    else:
        print(f"Total score for this hand: {total_score}")
    logging.info("Hand played")
    return total_score



def substitute_hand(hand, letter):
    """
    Substitute a letter.

    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    existing_letters = list(hand.keys())
    if letter in existing_letters:
        while True:
            substitute_letter = random.choice(alphabet)
            if substitute_letter not in existing_letters:
                letter_value = hand[letter]
                hand[substitute_letter] = letter_value
                del hand[letter]
                break
            else:
                continue
    else:
        pass
    logging.info("Subtitution was successfully done")


def play_game(word_list):
    replay = True
    full_total_score = 0
    while True:
        try:
            number_of_hands = int(input("Enter total number of hands: "))
            logging.debug(f"User choose number of hands: {number_of_hands}")
            break
        except ValueError:
            logging.error("Invalid input")
            print("Invalid input. Try to enter again!")
    while number_of_hands > 0:
        hand = deal_hand(HAND_SIZE)
        print("Current hand: ", end='')
        display_hand(hand)
        print()
        while True:
            asking_for_subtitude = input("Would you like to substitute a letter? ").lower()
            logging.debug(f"User choose whether do subtitution: {asking_for_subtitude}")
            if asking_for_subtitude == 'yes':
                letter = input("Which letter would you like to replace: ")
                logging.debug(f"User choose letter to replace: {letter}")
                substitute_hand(hand, letter)
                logging.info("Successful subtitution")
                break
            elif asking_for_subtitude == 'no':
                logging.info("No subtitution")
                break
            else:
                logging.error("Invalid input")
                pass
        print()
        total_score = play_hand(hand, word_list)
        print("--------")
        if replay is True:
            while True:
                asking_for_replay = input("Would you like to replay the hand? ").lower()
                logging.debug(f"User choose whether do replay: {asking_for_replay}")
                if asking_for_replay == 'yes':
                    print()
                    logging.info("Replay hand")
                    total_score2 = play_hand(hand, word_list)
                    replay = False
                    total_score = max(total_score, total_score2)
                    break
                elif asking_for_replay == 'no':
                    logging.info("No replay")
                    replay = True
                    break
                else:
                    logging.error("Invalid input")
                    pass
        full_total_score += total_score
        number_of_hands -= 1
        print()
    print(f"Total score over all hands: {full_total_score}")

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
