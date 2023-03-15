class Node:

    def __init__(self, key, val):
        self.key = key
        self.val = val

    def __gt__(self, other):
        return self.key < other.key

class HashTable:

    def __init__(self, table_size): # add appropriate attributes, NO default size
        ''' Initializes an empty hash table with a size that is the smallest
            prime number that is >= table_size (i.e. if 10 is passed, 11 will 
            be used, if 11 is passed, 11 will be used.)'''
        # initialize table size var
        self.table_size = table_size
        # creates hash table of size of next prime number of passed table size
        self.table = [None] * self.next_prime(self.table_size)
        # creates counter for the number of entries, starting at 0
        self.num_ent = 0

    def insert(self, key, value=None):
        ''' Inserts an entry into the hash table (using Horner hash function to determine index, 
        and quadratic probing to resolve collisions).
        The key is a string (a word) to be entered, and value is any object (e.g. Python List).
        If the key is not already in the table, the key is inserted along with the associated value
        If the key is is in the table, the new value replaces the existing value.
        If load factor is greater than 0.5 after an insertion, hash table size should be increased
        to the next prime greater than 2*table_size.'''
        # create node from key and val
        node = Node(key, value)
        # finds idx for value
        idx = self.horner_hash(key)
        # if key already in table, replace existing val
        if self.table[idx] is not None and self.table[idx].key == key:
            self.table[idx] = node
            return
        # initialize probing iterator
        idx_prob = 1
        # increase number of entries (after checking LF to ensure table is large enough)
        self.num_ent += 1
        # calculate load factor in case re-hash is needed
        load_factor = self.get_load_factor()
        # check if spot is already taken
        if self.table[idx] is not None:
            # loop through table using quadratic probing to find a place for the value if spot is taken
            while self.table[(idx + idx_prob) % self.get_table_size()] is not None:
                idx_prob = int((idx_prob ** (1/2) + 1) ** 2)
            self.table[(idx + idx_prob) % self.get_table_size()] = node
        # set val to key idx since spot is not already taken
        else:
            self.table[idx] = node

        if load_factor > 0.5:
            # self.insert(key, value)
            self.re_hash()

    def re_hash(self):
        # get length of the og table for the loop
        old_len = self.get_table_size()
        # create new table that self.table will be changed to
        new_table = [None] * (self.next_prime(old_len * 2))
        # set the length of the "current" table to the new table
        self.table_size = len(new_table)
        # loop through the entire current self.table
        for i in range(old_len):
            # get the key, value, index of the current spot if it is not None (node found)
            if self.table[i] is not None:
                key = self.table[i].key
                val = self.table[i].val
                idx = self.horner_hash(key)
                # print(idx, key, val)
                # attempt to add the Node to the new table
                if new_table[idx] is None:
                    new_table[idx] = Node(key, val)
                # if a Node is found in spot already, quad probe
                else:
                    idx_prob = 1
                    while new_table[int((idx + idx_prob) % self.get_table_size())] is not None:
                        idx_prob = (idx_prob ** (1 / 2) + 1) ** 2
                    new_table[int((idx + idx_prob) % self.get_table_size())] = Node(key, val)
        # set self.table to the new table
        self.table = new_table

    # compute the hash value by using Horner’s rule, as described in project specification.
    # this method should not mod with the table size
    def horner_hash(self, key):
        # sets key to first 8 char of key
        key = key[0:8]
        # finds n: already cannot be greater than 8 since key is edited, so just need to find len of the key
        n = len(key)
        # initialize hash value to 0 to be able to add
        hash_val = 0
        # loop through each char in the key and add the Horner val to total hash val
        for i in range(n):
            hash_val += ord(key[i]) * (31 ** (n - 1 - i))
        # mod by table size so the value will fit in the table
        hash_val = hash_val % self.get_table_size()
        # returns the hash_val sum
        return hash_val

    # find the next prime number that is > n
    # algorithm from GeeksForGeeks
    def next_prime(self, n):
        num = n
        # if num is already prime, returns the number
        if self.check_if_prime(num):
            return num
        # if num is 1 or less, next prime number has to be 2
        if num <= 1:
            return 2
        # initialize prime as "False"
        prime = False
        # loop until a prime number is found
        while not prime:
            # increase num each iteration
            num += 1
            # checks self.check_if_prime to return T/F if num is prime or not
            if self.check_if_prime(num):
                # sets "prime" to true if number is prime to exit loop
                prime = True
        # returns the prime number for the table size
        return num

    # helper function for self.next_prime()
    # algorithm from GeeksForGeeks
    def check_if_prime(self, num):
        # base case, if less than or equal to one it must be not Prime
        if num <= 1:
            return False
        # base case, if less than or equal to 3 (since <=1 is already False) then num must be Prime (2, 3)
        if num <= 3:
            return True
        if num % 2 == 0 or num % 3 == 0:
            return False
        # for loop to loop through all possible % vals to check if Prime or not
        for i in range(5, int((num + 1) ** (1 / 2)), 6):
            if num % i == 0 or num % (i + 2) == 0:
                return False
        # returns "True" if all if statements before do not already return False
        return True

    # returns True if key is in an entry of the hash table, False otherwise
    def in_table(self, key):
        # finds location of where the key SHOULD be
        idx = self.horner_hash(key)
        # checks table if the key is where it SHOULD BE, returns False is that spot is empty
        if self.table[idx] is None:
            return False
        elif self.table[idx].key == key:
            return True
        else:
            idx_prob = 1
            while self.table[(idx + idx_prob) % self.get_table_size()] is not None and \
                    self.table[(idx + idx_prob) % self.get_table_size()].key != key:
                idx_prob = int((idx_prob ** (1 / 2) + 1) ** 2)
            if self.table[(idx + idx_prob) % self.get_table_size()] is None:
                return False
            else:
                return True

    # returns the index of the hash table entry containing the provided key
    # if there is not an entry with the provided key, returns None
    def get_index(self, key):
        # gets horner idx for the key
        idx = self.horner_hash(key)
        # checks if table[idx] is None for base case
        if self.table[idx] is None:
            return None
        elif self.table[idx].key == key:
            return idx
        # checks if table[idx] is not None and also not the key (meaning yes entry at idx, but different key)
        elif self.table[idx].key is not key:
            # go through list using quad prob to either find
            idx_prob = 1
            # while loop to either find right key or reach None
            while self.table[int((idx + idx_prob) % self.get_table_size())] is not None and \
                    self.table[int((idx + idx_prob) % self.get_table_size())].key != key:
                idx_prob = (idx_prob ** (1/2) + 1) ** 2
            # returns idx if the spot is not None
            if self.table[int((idx + idx_prob) % self.get_table_size())] is not None and \
                    self.table[int((idx + idx_prob) % self.get_table_size())].key == key:
                return int((idx + idx_prob) % self.get_table_size())
            # after probing if still not found, then not there
            else:
                return None
        # if the spot already is the key, no prob needed, return idx

    # returns a Python list of all keys in the hash table
    def get_all_keys(self):
        # creates the python list to add keys
        key_lst = []
        # loops through entire hash table
        for i in range(self.get_table_size()):
            # checks if current spot at hash table has an entry
            if self.table[i] is not None:
                # if hash table has entry, add to python list of keys
                key_lst.append(self.table[i].key)
        # return python list of keys at the end of code
        return key_lst

    # returns the value associated with the key, if key is not in hash table, returns None
    def get_value(self, key):
        # set key to idx
        idx = self.horner_hash(key)
        if self.table[idx] is None:
            return None
        # check if there is an entry in the table at location key
        if self.table[idx] is not None:
            # returns the val at location key if it is not None
            if self.table[idx].key != key:
                idx_prob = 1
                while self.table[int((idx + idx_prob) % self.get_table_size())] is not None and \
                        self.table[int((idx + idx_prob) % self.get_table_size())].key != key:
                    idx_prob = (idx_prob ** (1 / 2) + 1) ** 2
                if self.table[int((idx + idx_prob) % self.get_table_size())] is not None:
                    return self.table[int((idx + idx_prob) % self.get_table_size())].val
            else:
                return self.table[idx].val
        # returns None if the value at key in the table is None

    # returns the number of entries in the table
    def get_num_items(self):
        return self.num_ent

    # returns the size of the hash table
    def get_table_size(self):
        # returns the length of the hash table
        return self.next_prime(self.table_size)

    # returns the load factor of the hash table (entries / table_size)
    def get_load_factor(self):
        # divides the number to entries by the table size to calculate the load factor
        return self.num_ent / self.get_table_size()
