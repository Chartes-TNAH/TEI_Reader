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


class TestPresenter(unittest.TestCase):
    def test_Presenter(self):
        doc = "Doc_test.xml"
        chemin_actuel = os.path.dirname(os.path.abspath(__file__))
        doc = etree.parse(os.path.join(chemin_actuel, doc))
        actual = presenter(doc)
        self.assertDictEqual(actual, {'Auteur': 'Alexandre Bartz', 'Date': '2020', 'Editeur': 'Oxygen',
                                      'Editeur_papier': 'Github', 'Lignes': '2', 'Personnages': ['Molière'],
                                      'Titre': 'Document test', 'Ville': 'Paris'})


if __name__ == '__main__':
    unittest.main()
