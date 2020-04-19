import unittest
from TEI_Reader.fonctions import *


class TestNormaliserNom(unittest.TestCase):
    def test_capitalize(self):
        actual = normaliser_nom("paris")
        self.assertEqual(actual, "Paris")

    def test_ponctuation(self):
        actual = normaliser_nom("@Paris!")
        self.assertEqual(actual, "Paris")

    def test_chaine_vide(self):
        actual = normaliser_nom("")
        self.assertEqual(actual, "")


class TestDecompte(unittest.TestCase):
    def test_decompte(self):
        actual = decompte(["Paris", "Berlin", "Paris", "Londres"])
        self.assertDictEqual(actual, {"Paris": 2, "Berlin": 1, "Londres": 1})

    def test_liste_vide(self):
        actual = decompte([])
        self.assertDictEqual(actual, {})

if __name__ == '__main__':
    unittest.main()
