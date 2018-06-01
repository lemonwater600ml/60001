# Problem Set 2, hangman.py
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
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    list_unique_secret_word = list(unique_letters(secret_word))
    list_unique_secret_word.sort()
    letters_guessed.sort()
    return list_unique_secret_word == letters_guessed  
    



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    present = []
    for letter in secret_word:
        if letter in letters_guessed:
            present.append(letter)
        else:
            present.append('_ ')
    present = ''.join(present)
    return present



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    available_letters = list(string.ascii_lowercase[:])
    for letter in letters_guessed:
        if letter in available_letters:
            available_letters.remove(letter)
    return ''.join(available_letters)
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guess_times = 6
    warning_times = 3
    letters_guessed = []
    letters_wrong_guessed = []
    print('Welcome to the game Hangman!')   #opening
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('You have', warning_times, 'warning left.')
    print('-------------')
    
    while is_word_guessed(secret_word, letters_guessed) is False and guess_times > 0 :
        #Assumes secret_word is str and letters_guessed is list.
        #Keep looping if guess_times > 0
        #...
        print('You have', guess_times, 'guesses left.')
        print('Available letters: ', get_available_letters(letters_guessed), end='')
        current_letter = str(input('Please guess a letter: ')).lower()
        
        if current_letter in secret_word:                  #right word
            if is_repeat(current_letter, letters_guessed, letters_wrong_guessed):               #repeat
                (warning_times, guess_times) = w_or_g_lost(warning_times, guess_times, letters_guessed)
            else:                                               #not repeat
                letters_guessed += current_letter
                print('Good guess:', get_guessed_word(secret_word, letters_guessed))
            
        else:                                              #wrong word
            if current_letter.isalpha():                        #is a alphabet
                if is_repeat(current_letter, letters_guessed, letters_wrong_guessed):   #repeat
                    (warning_times, guess_times) = w_or_g_lost(warning_times, guess_times, letters_guessed)
                else:                                           #not repeat
                    guess_times -= cv_g_lost(current_letter)
                    print('Oops! That letter is not in my word', get_guessed_word(secret_word, letters_guessed))
                    letters_wrong_guessed += current_letter
                        
            else:                                               #not a alphabet
                (warning_times, guess_times) = w_or_g_lost(warning_times, guess_times, letters_guessed)
                print('That is not a valid letter. You have', warning_times, 'warning left:', get_guessed_word(secret_word, letters_guessed))
       
        print('-------------')    
        current_letter = ''
    
    
    if is_word_guessed(secret_word, letters_guessed):
        total_score = guess_times * len(unique_letters(secret_word))
        print('Congratulation! Your score is', str(total_score) + ".")
    else:
        print('You lose! The word is', secret_word + '.')
        
    


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------
############1. if repeat checking with input and return
        ####2.       warning_lost with input and return to change variable
        ####
def is_repeat(current_letter, letters_guessed, letters_wrong_guessed):
    """Assumes current_letter, letters_guessed, letters_wrong_guessed are str or list,
    Return True if current is in letters_guessed or letters_wrong_guessed"""
    if current_letter in letters_guessed + letters_wrong_guessed:
        return True
    else:
        return False

def w_or_g_lost(warning_times, guess_times, letters_guessed):
    """Assumes warning_times and guess_times are int,
    If warning_times > 0, subtract 1 from warning_times; 
    subtract 1 from guess_time otherwise.
    """
    if warning_times > 0:
        warning_times -= 1
        print('Oops! You\'ve already guessed that letter. You have', warning_times, 'waring left:', get_guessed_word(secret_word, letters_guessed))
        return (warning_times, guess_times)
    else:
        guess_times -= 1
        print('Oops! You\'ve already guessed that letter. You have no warnings left so you lose one guess:', get_guessed_word(secret_word, letters_guessed))
        return (warning_times, guess_times)
   
        
        

def unique_letters(secret_word):
    """Assumes secret is a string.
    Return the number of nuique letters.
    """
    unique_dict = {}
    for letter in secret_word:
        if letter in unique_dict:
            unique_dict[letter] += 1
        else:
            unique_dict[letter] = 1  
    return unique_dict.keys()
    

def cv_g_lost(current_letter):
    """Assumes current_letter is a str.
    Return 2 if current_letter is Vowel; Otherwise return 1.
    """
    if current_letter in 'aeiou':
        return 2
    else:
        return 1

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    
    my_word = my_word.replace(' ', '')
    
    if len(my_word) != len(other_word):
        return False
    elif my_word == '': #The bug of asking hint without any guess remains.
        return False
    def same_check(my_word, other_word):
        if my_word == other_word:
            return True
        elif my_word[0] == '_' and len(my_word) == 1:
            return True
        elif my_word[0] == '_' and len(my_word) > 1:
            return True and same_check(my_word[1:], other_word[1:])
        else:
            return my_word[0] == other_word[0] and same_check(my_word[1:len(my_word)], other_word[1:len(other_word)])
    return same_check(my_word, other_word)
       



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
    
    my_word = my_word.replace(' ', '')
    candidate = []
    for word in wordlist:
        if len(word) == len(my_word): #same length
            candidate.append(word)
    candidate_count = candidate[:]
        
    for word_in_c in candidate_count:
        for i in range(len(my_word)):
            if my_word[i] != word_in_c[i] and my_word[i] != '_':
                candidate.remove(word_in_c)
                break
    if candidate == []:
        print('No matched found')
    else:
        print(' '.join(candidate))
        
    
            
            



def hangman_with_hints(secret_word):
    '''
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
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guess_times = 6
    warning_times = 3
    letters_guessed = []
    letters_wrong_guessed = []
    print('Welcome to the game Hangman!')   #opening
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('You have', warning_times, 'warning left.')
    print('-------------')
    
    while is_word_guessed(secret_word, letters_guessed) is False and guess_times > 0 :
        #Assumes secret_word is str and letters_guessed is list.
        #Keep looping if guess_times > 0
        #...
        print('You have', guess_times, 'guesses left.')
        print('Available letters: ', get_available_letters(letters_guessed), end='')
        current_letter = str(input('Please guess a letter: ')).lower()
        
        if current_letter in secret_word:                  #right word
            if is_repeat(current_letter, letters_guessed, letters_wrong_guessed):               #repeat
                (warning_times, guess_times) = w_or_g_lost(warning_times, guess_times, letters_guessed)
            else:                                               #not repeat
                letters_guessed += current_letter
                print('Good guess:', get_guessed_word(secret_word, letters_guessed))
            
        else:                                              #wrong word
            if current_letter.isalpha():                        #is a alphabet
                if is_repeat(current_letter, letters_guessed, letters_wrong_guessed):   #repeat
                    (warning_times, guess_times) = w_or_g_lost(warning_times, guess_times, letters_guessed)
                else:                                           #not repeat
                    guess_times -= cv_g_lost(current_letter)
                    print('Oops! That letter is not in my word', get_guessed_word(secret_word, letters_guessed))
                    letters_wrong_guessed += current_letter
                        
            else:                                               #not a alphabet
                if current_letter == '*':
                    if match_with_gaps(get_guessed_word(secret_word, letters_guessed), secret_word):
                        print('possible word matches are: ')
                        show_possible_matches(get_guessed_word(secret_word, letters_guessed))
                    else: #The bug of asking hint without any guess remains.
                        print('You don\'t even have a letter matched.')
                else:
                    (warning_times, guess_times) = w_or_g_lost(warning_times, guess_times, letters_guessed)
                    print('That is not a valid letter. You have', warning_times, 'warning left:', get_guessed_word(secret_word, letters_guessed))
       
        print('-------------')    
        current_letter = ''
    
    
    if is_word_guessed(secret_word, letters_guessed):
        total_score = guess_times * len(unique_letters(secret_word))
        print('Congratulation! Your score is', str(total_score) + ".")
    else:
        print('You lose! The word is', secret_word + '.')
        

    


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = 'tact' #choose_word(wordlist)
    #hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = 'apple'#choose_word(wordlist)
    hangman_with_hints(secret_word)
