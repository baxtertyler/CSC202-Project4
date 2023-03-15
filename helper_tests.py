import unittest
from hash_quad import *
from concordance import *


class TestList(unittest.TestCase):

    def test_next_prime_number(self):
        ht = HashTable(6)
        self.assertEqual(len(ht.table), 7)

    def test_stop_table(self):
        c = Concordance()
        c.load_stop_table("stop_words.txt")
        self.assertEqual(c.stop_table.in_table("and"), True)
        self.assertEqual(c.stop_table.get_index("and"), 211)

