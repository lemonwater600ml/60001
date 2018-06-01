# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)[:]

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_txt[:]

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        # initiate shift_dict
        shift_dict = self.get_normal_letter_dict(65).copy()
        assert 0 <= shift and shift <26, 'Range for shift is 0<= shift < 26.'
        # Uppercase
        for i in range(65, 91):                                     # for unit in get_normal_letter_dict in range 65~90
            if shift_dict[chr(i)] + shift >= 91:                        # if unit value + shift > 91
                shift_dict[chr(i)] = shift_dict[chr(i)] + shift -26         # unit value in shift_dict = value in get_normal_letter_dict + shift -26
            else:                                                       # else
                shift_dict[chr(i)] = shift_dict[chr(i)] + shift             # value = value + shift     
        # Lowercase
        for i in range(97, 123):                                    # for unit in get_normal_letter_dict in range 97~122
            if shift_dict[chr(i)] + shift >= 123 :                      # if unit value + shift > 122
                shift_dict[chr(i)] = shift_dict[chr(i)] + shift -26         # unit value in shift_dict = value in get_normal_letter_dict + shift -26
            else:                                                       # else
                shift_dict[chr(i)] = shift_dict[chr(i)] + shift             # value = value + shift     
        return shift_dict.copy()
        
    def get_normal_letter_dict(self, cha_num):   
        """ Assumes cha is a number :65
            originally be called by self.get_normal_letter_dict(65)
            Returns a diction contains a~z:97~122 and A~Z:65~90 by recursion"""
        whole_letter = {}
            
        if chr(cha_num) == 'Z':                                         # recursion stop at Z 90
            return {'Z':90, 'z':122}
        else:   
            whole_letter[chr(cha_num)] = cha_num                            # whole_letter assign chr 65 and chr 97
            whole_letter[chr(cha_num+32)] = cha_num+32 
            whole_letter.update(self.get_normal_letter_dict(cha_num+1))     # whole_letter.append()
            return whole_letter.copy()                                      #return the dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        #initialize
        shifted_message = ''
        shift_dict = self.build_shift_dict(shift).copy()
        
        for letter in self.message_text:                        # every letter in the message_text
            if letter.isalpha() is False:                           # change letter one by one according to shifted dict
                shifted_message += letter
            else:   
                shifted_message += chr(shift_dict[letter])
        return shifted_message
        
class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)
        

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        #return input('Enter a favor number for shift: ')
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()
        

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = input('Please Eneter a new integer for shift: ')


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)
        

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        
        num_matched = 0
        rank = {}
        sample = []
        best = 0

        for i in range(1, 26):                                          # make 26 version
            if len(Message.apply_shift(self, i).split(' ')) == 1:
                sample.extend(Message.apply_shift(self, i).split(' '))
            else:
                sample.extend(Message.apply_shift(self, i).split(' '))
            for word in sample:                                             # make dict to record and compare
                if is_word(Message.get_valid_words(self)  , word):
                    num_matched += 1
                    
            rank[i] = num_matched
            num_matched = 0
            sample = []
        for i in range(1, 26):                                          # find the best
            if rank[i] == max(rank.values()):
                best = int(i)
                break
        return (best, Message.apply_shift(self, best))
    
    def get_exerpt_from_Ciphertext(self, text):
        """ 
        Assumes text is a string including punctuation and blank space
        Returns a string without punctuation and blank space
        """
        text_list = []
        high = len(text)
        low = 0
        mid = (high+low)/2
        text = text.lower()
        text_ref = text[:]
        
        for unit in text_ref:                       # remove not alpha
            if unit.isalpha() is False:
                text.remove(unit)
        text_list = text[mid:mid + 100].split(' ')  # split the string into list by the blank space 
        text_list.remove(text_list[0])              # remove the first and the last word due to it may be a incomplete word
        text_list.remove(text_list[-1])
        return text_list                            # return the list 
        
if __name__ == '__main__':

    #Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    print('-----------')
    print('')

    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())
    print('-----------')
    print('')

    #TODO: WRITE YOUR TEST CASES HERE
    plaintext = PlaintextMessage('Tell me. \nWhat kind of the kind person you are?', 4)
    print('Expected Output: Xipp qi. \nAlex omrh sj xli omrh tivwsr csy evi?')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    print('-----------')
    print('')
    
    #TODO: best shift value and unencrypted story 
    ciphertext = CiphertextMessage('Xipp qi. \nAlex omrh sj xli omrh tivwsr csy evi?')
    print('Expected Output:', (22, 'Tell me. \nWhat kind of the kind person you are?'))
    print('Actual Output:', ciphertext.decrypt_message())
    print('-----------')
    print('')
    
