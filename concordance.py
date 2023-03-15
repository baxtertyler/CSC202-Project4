from hash_quad import *
import string


class Concordance:

    def __init__(self):
        self.stop_table = None          # hash table for stop words
        self.concordance_table = None   # hash table for concordance

    def load_stop_table(self, filename):
        """ Read stop words from input file (filename) and insert each word as a key into the stop words hash table.
        Starting size of hash table should be 191: self.stop_table = HashTable(191)
        If file does not exist, raise FileNotFoundError"""
        # try to open file, if file does not exist raise FileNotFoundError
        try:
            in_file = open(filename, "r")
        except FileNotFoundError as error:
            raise error
        # if error is not found
        else:
            # create stop table and create list of stop file
            self.stop_table = HashTable(191)
            lst = in_file.readlines()
            # loop through list of stop words and add them to the stop table
            for word in lst:
                self.stop_table.insert(word.strip())
        # close the stop file at the end of the function
        in_file.close()

    def load_concordance_table(self, filename):
        """ Read words from input text file (filename) and insert them into the concordance hash table, 
        after processing for punctuation, numbers and filtering out words that are in the stop words hash table.
        (The stop words hash table could possibly be None.)
        Do not include duplicate line numbers (word appearing on same line more than once, just one entry for that line)
        Starting size of hash table should be 191: self.concordance_table = HashTable(191)
        If file does not exist, raise FileNotFoundError"""
        # try to open file, if file does not exist raise FileNotFoundError
        try:
            in_file = open(filename, "r")
        except FileNotFoundError as error:
            raise error
        # if file was found
        else:
            # create hash table for concordance and create list of lines of file
            self.concordance_table = HashTable(191)
            lst = in_file.readlines()
            # loop through each line
            for i in range(len(lst)):
                # add line name for each line the loop loops through
                line = lst[i]
                # create the new line
                new_line = ""
                # loop through and add each char** to the new line
                for ch in line:
                    # if apostrophe, do not add to new line
                    if ch == "'" or ch == '\n':
                        continue
                    # if punctuation char, change char to space
                    elif ch in string.punctuation:
                        new_line += " "
                    # else add the char to the new str
                    else:
                        new_line += ch
                # split the line into a list of all the words in the line
                new_line = new_line.lower()
                lst_line = new_line.split()
                # loop through new list
                for word in lst_line:
                    # ensure word is not in stop table
                    if not self.stop_table.in_table(word):
                        # ensure word is not already in the concord table
                        if not self.concordance_table.in_table(word):
                            # ensure the word is a string and not other type
                            if word.isalpha():
                                # if all the 'if' statements pass, then add word to the concord table
                                self.concordance_table.insert(word, [i+1])
                        # if word already in concord table
                        else:
                            # create variable for line
                            var = self.concordance_table.get_value(word)
                            # ensure line is not repeated
                            if var[-1] != i+1:
                                # add line to value
                                var.append(i+1)
        in_file.close()

    def write_concordance(self, filename):
        """ Write the concordance entries to the output file(filename)
        See sample output files for format."""
        # open the outfile for writing
        out_file = open(filename, 'w')
        # create a list of all values in the concord table to
        new_list = []
        # loop through concord table to add acc inputs into the new list
        for node in self.concordance_table.table:
            if node is not None:
                new_list.append(node)
        # sort the list in descending order
        new_list = sorted(new_list, reverse=True)
        # loop through new list
        for node in new_list:
            # join all the values in the list to one string
            s = " ".join(map(str, node.val))
            # write the string to the outfile
            out_file.write(node.key + ": " + s + '\n')
        # close the outfile
        out_file.close()
