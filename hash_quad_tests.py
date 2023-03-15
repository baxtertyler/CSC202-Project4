import unittest
from hash_quad import *


class TestList(unittest.TestCase):

    def test_01a(self):
        ht = HashTable(6)
        ht.insert("cat", 5)
        self.assertEqual(ht.get_table_size(), 7)

    def test_01b(self):
        ht = HashTable(7)
        ht.insert("cat", 5)
        self.assertEqual(ht.get_num_items(), 1)

    def test_01c(self):
        ht = HashTable(7)
        ht.insert("cat", 5)
        self.assertAlmostEqual(ht.get_load_factor(), 1/7)

    def test_01d(self):
        ht = HashTable(7)
        ht.insert("cat", 5)
        self.assertEqual(ht.get_all_keys(), ["cat"])

    def test_01e(self):
        ht = HashTable(7)
        ht.insert("cat", 5)
        self.assertEqual(ht.in_table("cat"), True)
        self.assertEqual(ht.in_table("cffat"), False)

    def test_01f(self):
        ht = HashTable(7)
        ht.insert("cat", 5)
        self.assertEqual(ht.get_value("cat"), 5)
        self.assertEqual(ht.get_value("cagft"), None)
        self.assertEqual(ht.get_value("cagfht"), None)


    def test_01g(self):
        ht = HashTable(7)
        ht.insert("cat", 5)
        self.assertEqual(ht.get_index("cat"), 3)
        self.assertEqual(ht.get_index("cau"), None)


    def test_02(self):
        ht = HashTable(7)
        ht.insert("a", 0)
        self.assertEqual(ht.get_index("a"), 6)
        ht.insert("h", 0)
        self.assertEqual(ht.get_index("h"), 0)
        ht.insert("o", 0) 
        self.assertEqual(ht.get_index("o"), 3)
        ht.insert("v", 0)  # Causes rehash
        ht.insert("v", 1)
        self.assertEqual(ht.get_index("a"), 12)
        self.assertEqual(ht.get_index("h"), 2)
        self.assertEqual(ht.get_index("o"), 9)
        self.assertEqual(ht.get_index("v"), 16)


    def test_table_size(self):
        a = HashTable(1)
        self.assertEqual(a.get_table_size(), 2)
        b = HashTable(2)
        self.assertEqual(b.get_table_size(), 2)
        c = HashTable(5)
        self.assertEqual(c.get_table_size(), 5)
        d = HashTable(10)
        self.assertEqual(d.get_table_size(), 11)
        e = HashTable(20)
        self.assertEqual(e.get_table_size(), 23)
        f = HashTable(50)
        self.assertEqual(f.get_table_size(), 53)
        g = HashTable(100)
        self.assertEqual(g.get_table_size(), 101)
        h = HashTable(1000)
        self.assertEqual(h.get_table_size(), 1009)

    def test_prob_of_funcs(self):
        h = HashTable(3)
        h.insert("h", 1)
        self.assertEqual(h.get_index("h"), 2)
        self.assertEqual(h.in_table("h"), True)
        self.assertEqual(h.get_value("h"), 1)
        h.insert("a", 1)
        self.assertEqual(h.get_index("a"), 6)
        self.assertEqual(h.in_table("a"), True)
        self.assertEqual(h.get_value("a"), 1)
        # h.insert("o", 6)
        self.assertEqual(h.get_index("o"), None)
        self.assertEqual(h.in_table("o"), False)
        self.assertEqual(h.get_value("o"), None)
        h.insert("v", 1)
        self.assertEqual(h.get_index("v"), 3)
        self.assertEqual(h.in_table("v"), True)
        self.assertEqual(h.get_value("v"), 1)

    def test_prob_of_funcs2(self):
        h = HashTable(7)
        h.insert("h", 1)
        self.assertEqual(h.get_index("h"), 6)
        self.assertEqual(h.in_table("h"), True)
        self.assertEqual(h.get_value("h"), 1)
        h.insert("a", 1)
        self.assertEqual(h.get_index("a"), 0)
        self.assertEqual(h.in_table("a"), True)
        self.assertEqual(h.get_value("a"), 1)
        h.insert("o")
        self.assertEqual(h.get_index("o"), 3)
        self.assertEqual(h.in_table("o"), True)
        self.assertEqual(h.get_value("o"), None)
        h.insert("v", 2)
        self.assertEqual(h.get_index("v"), 16)
        self.assertEqual(h.in_table("v"), True)
        self.assertEqual(h.get_value("v"), 2)
        h.insert("gf", 3)
        h.insert("gtrf", 3)
        h.insert("grf", 3)
        h.insert("gkjhf", 3)
        h.insert("gf", 3)
        h.insert("gtgfrf", 3)
        h.insert("grgfdf", 3)
        h.insert("gkfdjhf", 3)
        h.insert("gref", 3)
        h.insert("gt76wrf", 3)
        h.insert("grewrf", 3)
        h.insert("gkjfdthf", 3)
        h.insert("gfr", 3)
        h.insert("gtretrf", 3)
        h.insert("grhgf", 3)
        h.insert("gbvckjhf", 3)

    def test_horner_function(self):
        h = HashTable(10)
        h.insert("aaaaa", 0)
        h.insert("aaaaa", 1)
        h.insert("aaaaa", 4)
        h.insert("aaaaa", 9)
        h.insert("aaaaa", 16)
        h.insert("aaaaa", 25)

    def test_same_key(self):
        ht = HashTable(5)
        ht.insert("a", 1)
        self.assertEqual(ht.get_value("a"), 1)
        ht.insert("a", 2)
        self.assertEqual(ht.get_value("a"), 2)






if __name__ == '__main__':
   unittest.main()
