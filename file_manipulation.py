import statistics


class FileManipulation:
    def __init__(self, file_path, file_name):
        self.__file_path = file_path
        self.__file_name = file_name
        self.__file_as_sentences = []
        self.__file_as_list = []
        self.__words_dict = {}

    def get_file_path(self):
        return self.__file_path

    def set_file_path(self, file_path):
        self.__file_path = file_path

    def get_file_name(self):
        return self.__file_name

    def set_file_name(self, name):
        self.__file_name = name

    '''
    This function reads each line of the file, remove duplicated spaces and convert the line to a list 0f words.
    '''

    def open_file(self):
        # to count the sentences' length
        file_as_string = open(self.__file_path, 'r').read()
        self.__file_as_sentences = file_as_string.split('.')
        self.__file_as_sentences = [' '.join(sentence.split()).split() for sentence in self.__file_as_sentences]
        with open(self.__file_path, 'r') as self.__file_name:
            for line in self.__file_name:
                # check that the line is not empty
                if line.strip():
                    # replace all multiple spaces with one space
                    line_with_single_spaces = ' '.join(line.split())
                    # create array from words separated by spaces
                    line_separated_by_spaces = line_with_single_spaces.split()
                    # add the line to a list of lines
                    self.__file_as_list.append(line_separated_by_spaces)

    '''
    @return the longest sentence length
    '''

    def get_longest_sentence_length(self):
        return max(len(line) for line in self.__file_as_sentences)

    '''
    @return then average of sentences' lengths
    '''

    def get_sentence_mean_length(self):
        return statistics.mean(len(line) for line in self.__file_as_sentences)

    '''
    @return the amount of lines in the file
    '''

    def get_lines_amount(self):
        return len(self.__file_as_list)

    '''
    @return the amount of words in the file
    '''

    def get_words_amount(self):
        words_amount = 0
        for line in self.__file_as_list:
            words_amount += len(line)
        return words_amount

    '''
    @return the amount of distinct words in the file
    '''

    def get_distinct_words_amount(self):
        # check if words exists in the words dictionary
        if not self.__words_dict:
            self.__insert_data_into_dict()
        return len(self.__words_dict.keys())

    '''
    This function takes a raw line and removes all punctuation(commas,dashes, etc) from words and from line
    @param line as a list of words
    @return the same line without punctuation
    '''

    def __organize_line(self, line):
        # final list with all words that contains at least one alphabet character
        remained_list = []
        for i, word in enumerate(line):
            # check if the word contain at least one alphabet character
            if not any(letter.isalpha() for letter in word):
                continue
            # remove punctuation from the first and the end of a word
            if not word[-1].isalpha():
                word = word[:-1]
            if not word[0].isalpha():
                word = word[1:]
            remained_list.append(word)
        return remained_list

    '''
    This function inserts all words to a dictionary
    '''

    def __insert_data_into_dict(self):
        for line in self.__file_as_list:
            # first remove all punctuation from the line and word
            line = self.__organize_line(line)
            for word in line:
                word = word.lower()
                # check if the word already exists in the words' dictionary
                if self.__words_dict.get(word) is not None:
                    self.__words_dict[word] += 1
                # if the word doesn't exist, its being added to the dictionary
                else:
                    self.__words_dict[word] = 1

    '''
    This function returns the longest sequence in the file that doesn't contain a given letter
    @param k the letter that wished not to be seen
    @return the longest sequence without the given letter
    '''

    def get_longest_sequence_without_k(self, k):
        max_length = 0
        temp_first_index = (0, 0)
        first_index = (0, 0)
        last_index = (0, 0)
        counter = 0
        for i, line in enumerate(self.__file_as_list):
            for j, word in enumerate(line):
                # check if the word contains at least one alphabetical character
                if not any(letter.isalpha() for letter in word):
                    continue
                # check if the current word contains the given letter
                if k.lower() not in word.lower():
                    # if the word doesn't contain the letter and this is the first time that the letter hasn't been seen
                    if counter == 0:
                        # assign the in current index to be the temporary first index
                        temp_first_index = (i, j)
                    # anyway, increase the counter of consecutive words without k by one
                    counter += 1
                # in case the word contains the letter, so compare the current counter with the longest sequence so far
                elif counter > max_length:
                    # if the current counter is longest then the previous on, change the max_length to be the counter
                    max_length = counter
                    # change the first index to be the temporary one
                    first_index = temp_first_index
                    # check if the word is the first in a line
                    if j == 0:
                        # the last word which didn't contain the letter is the last in the previous line
                        last_index = (i - 1, len(self.__file_as_list[i - 1]) - 1)
                    else:
                        # the last word that didn't contain the letter is the previous word in the line
                        last_index = (i, j - 1)
                    counter = 0
                # anyway, start to count from scratch
                else:
                    counter = 0
        # edge case, when the file ends with word that doesn't contain the letter
        if counter > max_length:
            # if current counter bigger then the max_length
            max_length = counter
            # last index is the last word in the last line
            last_index = (len(self.__file_as_list) - 1, len(self.__file_as_list[-1]) - 1)
        # call the function that will return the desired sequence
        return self.__extract_longest_seq_without_k(first_index[0], first_index[1], last_index, max_length)

    '''
    This function return a sequence in the file between two given indexes
    @param i index of line to start
    @param j index of word to start
    @param last_index till what line and word to return 
    @param max length length of sequence to return 
    @return the desired sequence
    '''

    def __extract_longest_seq_without_k(self, i, j, last_index, max_length):
        # the list that will be returned
        final_list = []
        # run through the lines from the given line
        while i <= last_index[0]:
            # run through the words till the amount of words that has been given
            while j < len(self.__file_as_list[i]) and max_length > 0:
                max_length -= 1
                final_list.append(self.__file_as_list[i][j])
                j += 1
            i += 1
            j = 0
        # remove all unnecessary punctuation from the sequence
        final_list = self.__organize_line(final_list)
        # return the sequence as a string
        return ' '.join(final_list)

    '''
    This function counts appearances of basic colors in the file
    @return list with each colors and a number of its appearances in the file
    '''

    def get_occurrences_of_colors(self):
        basic_colors_list = ['red', 'blue', 'green', 'yellow', 'purple', 'pink', 'orange', 'brown', 'black', 'white',
                             'gray', 'gold', 'silver', 'beige']
        # list that will be returned
        final_list = []
        # check if the words have been inserted to the words' dictionary
        if not self.__words_dict:
            # if not, call a function to insert the words
            self.__insert_data_into_dict()
        # run through the words in the dictionary
        for key, value in self.__words_dict.items():
            # check if the words is one of the basic colors
            if key in basic_colors_list:
                final_list.append(f'{key} : {value}')
        return final_list
