# import required libraries and dependencies

import string
import pandas as pd

# read text corpus from the file
# append words to corpora_words list
# return total words list

# def read_corpora(read_file_name):
#   corpora_words = []
#   with open(file_name, "r") as file:
#     lines = file.readlines()
#     for line in lines:
#       corpora_words += re.findall(r'\w+', line.lower())
#   return corpora_words

# # specify file path and call read_corpora
# # assign unique tokens in vocab

# file_name = 'large.txt'
# # words = read_corpora(file_name)
# # vocab = set(words)
# w_freq = Counter(read_corpora(file_name))                                       

# # print(f"There are {len(words)} total words in the corpus")
# # print(f"There are {len(vocab)} unique words in the vocabulary")

# # write the word list to file 'write_large.csv' for future purpose 

# with open('write_large.csv', mode='w') as csv_file:
#   fieldnames = ['WORD', 'COUNT']
#   writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#   writer.writeheader()
#   for key in w_freq:
#     writer.writerow({'WORD':key, 'COUNT':w_freq[key]})
    
# define a spell checker class
# initialize pre calculated values
# perform edit operations
# call check function to get the guessed words list 
# call edit distance = 1
# if call empty, call edit distance = 2
# if call empty, call edit distance = 3

class SpellChecker(object):

  def __init__(self):
    df = pd.read_csv('write_large.csv')
    self.vocabulary = set(df['WORD'])                                           # set of unique tokens
    self.word_frequency = dict(zip(df.WORD, df.COUNT))                          # frequency of each occuring word
    total_word_count = float(sum(self.word_frequency.values()))                 # total corpus word count
    self.likelihood = {word: (self.word_frequency[word] / total_word_count) for word in self.vocabulary}
                                                                                # calculates each word's likelihood
                                                                                # forms a dictionary key = word, value = likelihood
    self.set_1, self.set_2, self.set_3 = {}, {}, {}                             # set to store distance edited words

  def edit_dist_one(self, word):
    characters = string.ascii_lowercase                                         # returns a string of alphabets
    
    # perform word split operation
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    
    # perform single character insert operation
    inserts = [left + char + right for left, right in splits for char in characters] 
    
    # perform single character delete operation
    deletes = [left + right[1:] for left, right in splits if (right)]

    # perform single character replace operation
    replaces = [left + char + right[1:] for left, right in splits if (right) for char in characters]

    # perform adjacent character swap operation
    swaps = [left + right[1] + right[0] + right[2:] for left, right in splits if (len(right) > 1)] 
    
    self.set_1 = set(inserts + deletes + replaces + swaps)                      # form a set of resultant words
    valid_set_1 = set(word for word in self.set_1 if word in self.vocabulary)   # check for validity of words in set
    return valid_set_1

  def edit_dist_two(self, word):

    # form a set of words by recalling edit operations on set_1
    self.set_2 = set(ele_2 for ele_1 in self.set_1 for ele_2 in self.edit_dist_one(ele_1))
    valid_set_2 = set(word for word in self.set_2 if word in self.vocabulary)   # check for validity of words in set
    return valid_set_2

  def edit_dist_three(self, word):

    # form a set of words by recalling edit operations on set_2
    self.set_3 = set(ele_3 for ele_2 in self.set_2 for ele_3 in self.edit_dist_one(ele_2))
    valid_set_3 = set(word for word in self.set_3 if word in self.vocabulary)   # check for validity of words in set
    return valid_set_3

  def edit_dist_four(self, word):

    # form a set of words by recalling edit operations on set_3
    set_4 = set(ele_4 for ele_3 in self.set_3 for ele_4 in self.edit_dist_one(ele_3))
    valid_set_4 = set(word for word in set_4 if word in self.vocabulary)        # check for validity of words in set
    return valid_set_4

  def check(self, word):
    guess_word_list = []                                                        # list of tuples with [(word, likelihood)]
    valid_candidates = set()                                                    # set of guesses

    # if word already present in the dictionary, assign highest likelihood to the word itself
    if word in self.vocabulary:                                                     
      guess_word_list += [(word, 1.0)]
      valid_candidates.add(word)

    #### deprecated code, can examine later ####                                        
    # valid_candidates = self.edit_dist_one(word) or self.edit_dist_two(word) or [word] or self.edit_distance_three(word) or self.edit_distance_three(word)
    # valid_candidates = list(self.edit_dist_one(word))
    # if (len(valid_candidates) < 5):
    #   valid_candidates += list(self.edit_dist_two(word))
    # if (len(valid_candidates) < 5):
    #   valid_candidates += [word]
    # if (len(valid_candidates) < 5):
    #   valid_candidates += list(self.edit_dist_three(word))
    # if (len(valid_candidates) < 5):
    #   valid_candidates += list(self.edit_dist_four(word))
    # valid_candidates = set(valid_candidates)

    # list of probable candidates for typed word
    # sort the valid candidates in descending order
    valid_can_1 = self.edit_dist_one(word)
    guess_word_list += sorted([(w, self.likelihood[w]) for w in valid_can_1 if w not in valid_candidates], key = lambda tup : tup[1], reverse = True)
    valid_candidates = valid_can_1

    if (len(valid_candidates) < 3):                                             # nested ifs to reduce runtime
      valid_can_2 = self.edit_dist_two(word)
      guess_word_list += sorted([(w, self.likelihood[w]) for w in valid_can_2 if w not in valid_candidates], key = lambda tup : tup[1], reverse = True)
      valid_candidates.update(valid_can_2)

      if (len(valid_candidates) < 3 and word not in self.vocabulary):           # level 1
        guess_word_list += [(word, 0.0)]
        valid_candidates.add(word)

        if (len(valid_candidates) < 3):                                         # level 2
          valid_can_3 = self.edit_dist_three(word)
          guess_word_list += sorted([(w, self.likelihood[w]) for w in valid_can_3 if w not in valid_candidates], key = lambda tup : tup[1], reverse = True)
          valid_candidates.update(valid_can_3)

          if (len(valid_candidates) < 3):                                       # level 3
            valid_can_4 = self.edit_dist_four(word)
            guess_word_list += sorted([(w, self.likelihood[w]) for w in valid_can_4 if w not in valid_candidates], key = lambda tup : tup[1], reverse = True)
            valid_candidates.update(valid_can_4)

    # guess_word_list = list(set(guess_word_list))                              # remove redundant words
    
    # if edit distance doesn't return desired guesses return most probable words from dictionary
    if (len(guess_word_list) < 3):                                     
      index = 3 - len(guess_word_list)
      valid_can_5 = set([w for w in self.vocabulary if str(w)[0] == word[0]][:index])
      guess_word_list += sorted([(w, self.likelihood[w]) for w in valid_can_5 if w not in valid_candidates], key = lambda tup : tup[1], reverse = True)

    top_guesses = [w[0] for w in guess_word_list]                               # top guesses from the guess words' list
    return tuple(top_guesses[:3])                                               # return top five guesses

# create a class instance
# call object.check() function for each typed word

spellchecker = SpellChecker()

# check_string = 'jpsdfykjnk'
# check_string = check_string.lower()
# check_list = check_string.split(sep=' ')

# for s in check_list:
#   print(spellchecker.check(s))