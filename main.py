# hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
from typing import Any

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
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
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program

wordlist = load_words()

def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    if len(letters_guessed) == 0:
        return False
    guessed_word = get_guessed_word(secret_word, letters_guessed)
    for i in range (len(guessed_word)):
        try:
            if guessed_word[i] == "_":
                return False
        except IndexError:
            pass
    return True

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ''
    for i in range (len(secret_word)):
        is_guessed = False
        for j in range (len(letters_guessed)):
           try:
                if secret_word[i] == letters_guessed[j][0]:
                    guessed_word = guessed_word + letters_guessed[j]
                    guessed_word = guessed_word + " "
                    is_guessed = True
           except IndexError:
               pass
        if is_guessed != True:
            guessed_word = guessed_word + "_ "
    return guessed_word

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = "abcdefghijklmnopqrstuvwxyz"
    letters_guessed = list(letters_guessed)

    for i in range (len(available_letters)):
        for j in range (len(letters_guessed)):
            try:
                if available_letters[i] == letters_guessed[j][0]:
                    available_letters = available_letters.replace(available_letters[i], "")
            except:
                pass
    return available_letters

def calculate_score(secret_word,guesses_left):
    in_word = []
    for i in range (len(secret_word)):
        if secret_word[i] not in in_word:
            in_word.append(secret_word[i])
    return len(in_word) * guesses_left

def hangman(secret_word):

    # FILL IN YOUR CODE HERE AND DELETE "pass"
    secret_word = secret_word
    guesses_left = 6
    warnings_left = 3
    letters_guessed = list()
    current_word = get_guessed_word(secret_word, letters_guessed)
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print("------------------")
    while guesses_left > 0 and not is_word_guessed(secret_word, letters_guessed):
        print("You have", guesses_left, "guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        current_guess = input("Please guess a letter: ").lower()
        if current_guess in string.ascii_lowercase:
            if current_guess in get_available_letters(letters_guessed):
                last_word = get_guessed_word(secret_word, letters_guessed)
                letters_guessed.append(current_guess)
                current_word = get_guessed_word(secret_word, letters_guessed)
                if last_word == current_word:
                    if current_guess in ["a", "e", "i", "o", "u"]:
                        guesses_left -= 2
                    else:
                        guesses_left -= 1
                    print(f"Oops! That letter is not in my word: {current_word}")
                else:
                    print(f"Good guess: {current_word}")

            else:
                if warnings_left > 0:
                    warnings_left -= 1
                    print(f"You have already guessed this letter. You have {warnings_left} warnings left.")
                else:
                    guesses_left -= 1
                    print("You have already guessed this letter. You have no warnings left, so you lose one guess.")
        else:
            if warnings_left > 0:
                warnings_left -= 1
                print(f"Ooops! That is not a valid letter. You have {warnings_left} warnings left.")
            else:
                guesses_left -= 1
                print("Ooops! That is not a valid letter. you have no warnings left, so you lose a guess.")
        print("------------------")
    if is_word_guessed(secret_word, letters_guessed):
        print("Congratulations, you won!")
        print(f"Your total score for this game is: {calculate_score(secret_word, guesses_left)}")
    else:
        print("Sorry, you ran out of guesses! The word was ", secret_word, ".")

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    guessed_word = my_word.replace(" ", "")
    if len(guessed_word) == len(other_word):
        for i in range(len(my_word)):
            try:
                if guessed_word[i] == other_word[i] or guessed_word[i] == "_":
                    continue
                return False
            except:
                continue
        return True
    else:
        return False



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    possible_matches = ""
    for i in range (len(wordlist)):
        if match_with_gaps(my_word, wordlist[i]):
            possible_matches = possible_matches + wordlist[i]
            possible_matches = possible_matches + " "
    return possible_matches



def hangman_with_hints(secret_word):

    # FILL IN YOUR CODE HERE AND DELETE "pass"
    secret_word = secret_word
    guesses_left = 6
    warnings_left = 3
    letters_guessed = list()
    current_word = get_guessed_word(secret_word, letters_guessed)
    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print("------------------")
    while guesses_left > 0 and not is_word_guessed(secret_word, letters_guessed):
        print("You have", guesses_left, "guesses left.")
        print(f"Available letters: {get_available_letters(letters_guessed)}")
        current_guess = input("Please guess a letter: ").lower()
        if current_guess in string.ascii_lowercase:
            if current_guess in get_available_letters(letters_guessed):
                last_word = get_guessed_word(secret_word, letters_guessed)
                letters_guessed.append(current_guess)
                current_word = get_guessed_word(secret_word, letters_guessed)
                if last_word == current_word:
                    if current_guess in ["a", "e", "i", "o", "u"]:
                        guesses_left -= 2
                    else:
                        guesses_left -= 1
                    print(f"Oops! That letter is not in my word: {current_word}")
                else:
                    print(f"Good guess: {current_word}")

            else:
                if warnings_left > 0:
                    warnings_left -= 1
                    print(f"You have already guessed this letter. You have {warnings_left} warnings left.")
                else:
                    guesses_left -= 1
                    print("You have already guessed this letter. You have no warnings left, so you lose one guess.")
        else:
            if current_guess == "*":
                print("Possible word matches are: ")
                print(show_possible_matches(current_word))
            else:
                if warnings_left > 0:
                    warnings_left -= 1
                    print(f"Ooops! That is not a valid letter. You have {warnings_left} warnings left.")
                else:
                    guesses_left -= 1
                    print("Ooops! That is not a valid letter. you have no warnings left, so you lose a guess.")
        print("------------------")
    if is_word_guessed(secret_word, letters_guessed):
        print("Congratulations, you won!")
        print(f"Your total score for this game is: {calculate_score(secret_word, guesses_left)}")
    else:
        print("Sorry, you ran out of guesses! The word was ", secret_word, ".")



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    hangman(secret_word)


###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
