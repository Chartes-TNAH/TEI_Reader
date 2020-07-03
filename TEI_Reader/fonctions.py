# Ce module permet de lister tous les fichiers d'un dossier.
from flask import url_for

# Ce module permet d'utiliser des expressions régulières en python.
import re

# Ce module petmet d'accéder au système de fichiers.
import os

# Cette librairie permet de parser du XML en python.
from lxml import etree

# Cette librairie est utile pour analyser les textes, j'y ajoute cependant encore quelques "stop words" qui ne me
# semblent pas pertinents pour l'analyse textuelle que je propose.
from stop_words import get_stop_words
stop_words = get_stop_words('fr')
stop_words.extend(["jai", "d", "", "quil", "cest", "dun", "sil", "quun", "quune", "quon", "dune", "nest", "oui", "non",
                   "lon", "jen", "quà", "men", "quen", "jy", "na", "peutetre", "peutêtre", "nen", "lautre", "toute",
                   "plus", "va"])

# Dès qu'on utilise du XPath, il est nécessaire de préciser le namespace, on le met donc dans une variable.
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

# Fonctions servant à la mise en place des index :

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CORPORA = {}
with open(os.path.join(ROOT_DIR, "data", "corpus_list.xml")) as f:
    xml = etree.parse(f)
    for corp in xml.xpath("//corpus"):
        file = corp.attrib["path"]
        corpus_id = corp.attrib["id"].strip()
        CORPORA[corpus_id] = file


def normaliser_nom(mot):
    """ Cette fonction permet de normaliser les noms de personnages ou de lieux en retirant les marques de ponctuation.

    :param mot: une chaîne de caractères
    :return: nom normalisé
    :rtype: string
    """
    ponctuation = '!@#$%^&*()_-+={}[]:;"\'|<>,.?/~`’'
    for marqueur in ponctuation:
        mot = mot.replace(marqueur, "")
        mot = mot.capitalize()
    return mot


def index_personnages(doc):
    """ Fonction qui permet d'obtenir un index des personnages.

    :param doc: un chemin de fichier
    :return: un dictionnaire ayant pour clefs les noms de personnages et pour valeurs une liste avec les occurences
    de chaque personnage
    :rtype: dict
    """
    index = {}
    # On ne prend en compte que les l descendants de body et ayant un attribut
    lignes = doc.xpath('//tei:body//tei:l[@*]', namespaces=ns)

    ligne_precedente = None
    for ligne in lignes:
        """ Pour chaque ligne dotée d'un attribut 'n', on récupère sa valeur. Ce if est nécessaire puisque certaine
        ligne, notamment les stichomyties, ont uniquement un attribut 'part' : on récupère donc le numéro de
        la ligne précédente. """
        if ligne.get("n"):
            numero_de_ligne = ligne.get("n")
        else:
            numero_de_ligne = ligne_precedente

        noms_pers = ligne.xpath('.//tei:reg/tei:persName/text()', namespaces=ns)

        # On récupère ensuite pour chacune de ses lignes le nom du personnage associé, via l'élément 'persName'
        for nom_pers in noms_pers:
            nom_pers = normaliser_nom(nom_pers)
            if nom_pers not in index:
                index[nom_pers] = []

            index[nom_pers].append(numero_de_ligne)

        ligne_precedente = numero_de_ligne
    return index


def index_lieux(doc):
    """ Fonction qui permet d'obtenir un index des lieux.

       :param doc: un chemin de fichier
       :return: un dictionnaire ayant pour clefs les noms de lieux et pour valeurs une liste avec les occurences
       de chaque lieu
       :rtype: dict
       """
    index = {}
    # On ne prend en compte que les l descendants de body et ayant un attribut, quel qu'il soit puisque seuls les
    # éléments 'l' du 'body' ont un attribut.
    lignes = doc.xpath('//tei:body//tei:l[@*]', namespaces=ns)

    ligne_precedente = None
    for ligne in lignes:
        # Il s'agit ici du même code que la fonction index_personnages puisque l'on peut rencontrer les mêmes
        # problèmes de lignes déjà expliqués.
        if ligne.get("n"):
            numero_de_ligne = ligne.get("n")
        else:
            numero_de_ligne = ligne_precedente

        noms_lieux = ligne.xpath('.//tei:reg/tei:placeName/text()', namespaces=ns)

        # On récupère ensuite pour chacune de ses lignes le nom du lieu associé, via l'élément 'placeName'
        for nom_lieu in noms_lieux:
            nom_lieu = normaliser_nom(nom_lieu)
            if nom_lieu not in index:
                index[nom_lieu] = []

            index[nom_lieu].append(numero_de_ligne)

        ligne_precedente = numero_de_ligne
    return index


# Fonction permet de générer la table des matières :

def table_des_matieres(doc):
    """ Fonction qui permet d'obtenir une table des matières de chaque document

       :param doc: un chemin de fichier
       :return: une liste de dictionnaires, il y a un dictionnaire par acte. Les scènes sont elles-mêmes comprises
       dans une liste de dictionnaires qui a pour clefs 'Titre' et 'Personnages'.
       :rtype: list
       """
    actes = doc.xpath("//tei:div[@type='act']", namespaces=ns)
    tdm = []

    for acte in actes:
        # Pour ne pas obtenir de liste mais uniquement le premier élément de la liste, même chose pour les scènes
        titre_acte = acte.xpath('./tei:head/text()', namespaces=ns)[0]
        # Le corpus ne permet pas de préciser l'attribut de l'élément 'div' (@type="scene") puisque tous les fichiers du
        # corpus n'en ont pas. On suppose donc que chaque 'div' qui suit une 'div[@type="act"]' est une scène
        scenes = acte.xpath('./tei:div', namespaces=ns)

        tdm_scene = []
        speaker = []
        # On récupère tous les speaker puis on utilise le type set() pour n'en garder qu'un. Cette méthode m'a paru
        # être la meilleure puisque lorsque la scène est un monologue, il n'y a pas d'éléments 'stage' or l'élément
        # 'speaker' est présent quel que soit le nombre de personnage(s).
        for scene in scenes:
            titre_scene = scene.xpath('./tei:head/text()', namespaces=ns)[0]
            personnages = set(scene.xpath('.//tei:speaker/text()', namespaces=ns))

            # On normalise le nom de chaque personnage (notamment afin d'enlever les signes de ponctuation qui
            # pourraient fausser le set.
            for personnage in personnages:
                personnage = normaliser_nom(personnage)
                speaker.append(personnage)

            # Pour chaque scène, on stocke dans un dictionnaire le titre (clef 1) et les personnages (clef 2).
            tdm_scene.append({
                "Titre": titre_scene,
                "Personnages": set(speaker)
            })

        # Pour chaque acte, on stocke dans un dictionnaire le titre (clef 1) et la liste des scènes précedemment
        # constituée
        tdm.append({
            "Titre": titre_acte,
            "Scènes": tdm_scene
        })

    return tdm


# Fonctions qui permettent de présenter le document :

def remove_element(el):
    """
    Fonction qui permet de supprimer un élément dans l'arbre XML sans supprimer pour autant le texte qui suit
    :param el: un élément xml
    """
    # On commence par récupérer l'élément parent.
    parent = el.getparent()
    # Si cet élément contient du texte et que le texte n'est pas nul :
    if el.tail and el.tail.strip():
        # On récupère l'élément précédent.
        prev = el.getprevious()
        # S'il y en a un :
        if prev:
            # On concatène la "tail" de l'élément précédent avec celle de l'élément à supprimer.
            prev.tail = (prev.tail or '') + el.tail
        else:
            # On ajoute la "tail" de l'élément à supprimer au texte de l'élément parent.
            parent.text = (parent.text or '') + el.tail
    # On supprime ensuite l'élément entré en paramètre.
    parent.remove(el)


def presenter(doc):
    """
    Cette fonction permet d'obtenir des informations déterminées sur chaque document

    :param doc: un chemin de fichier
    :return: un dictionnaire contenant le titre, l'auteur, l'éditeur électronique, la date et le lieu de publication
    ainsi que le nom de l'éditeur papier
    :rtype: dict
    """
    titre = doc.xpath('//tei:titleStmt/tei:title/text()', namespaces=ns)[0]
    auteur = doc.xpath('//tei:titleStmt/tei:author/text()', namespaces=ns)[0]
    editeur = doc.xpath('//tei:titleStmt/tei:editor/text()', namespaces=ns)[0]
    date = doc.xpath('//tei:sourceDesc//tei:date/text()', namespaces=ns)[0]
    ville = doc.xpath('//tei:sourceDesc//tei:pubPlace/text()', namespaces=ns)[0]
    editeur_papier = doc.xpath('//tei:sourceDesc//tei:publisher/text()', namespaces=ns)[0]

    lignes = doc.xpath('//tei:l[@n]', namespaces=ns)
    derniere_ligne = lignes[-1]
    derniere_ligne = derniere_ligne.get("n")

    for lb in doc.xpath("//tei:castList//tei:lb", namespaces=ns):
        remove_element(lb)
    for c in doc.xpath("//tei:c", namespaces=ns):
        remove_element(c)

    personnages = doc.xpath('//tei:castItem/text()', namespaces=ns)

    return {
        "Titre": titre,
        "Auteur": auteur,
        "Editeur": editeur,
        "Date": date,
        "Ville": ville,
        "Editeur_papier": editeur_papier,
        "Lignes": derniere_ligne,
        "Personnages": personnages
    }


def ouvrir_doc(file_id):
    """
    Cette fonction permet d'ouvrir un document

    :param file_id: ID d'un fichier présent dans corpus_list.xml4
    :return: le même fichier parsé par etree
    """
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    return etree.parse(os.path.join(chemin_actuel, "data", CORPORA[file_id]))


def corpus():
    """
    Cette fonction permet d'obtenir la liste de tous les fichiers présents dans le corpus étudié

    :return: liste de dictionnaires (un dictionnaire par oeuvre, contenant le nom du fichier, le titre et l'auteur)
    :rtype: list
    """
    liste_titre = []
    for corpus_id, file in CORPORA.items():
        doc = ouvrir_doc(corpus_id)
        titre = doc.xpath('//tei:titleStmt/tei:title/text()', namespaces=ns)[0]
        auteur = doc.xpath('//tei:titleStmt/tei:author/text()', namespaces=ns)[0]
        liste_titre.append({
            "Fichier": corpus_id,
            "Titre": titre,
            "Auteur": auteur
        })
    return liste_titre


# Fonctions servant à l'analyse du texte :

def normalisation(mot):
    """
    Cette fonction permet de normaliser les mots en retirant les marques de ponctuation et en normalisant la casse
    :param mot: une chaîne de caractères
    :return: mot normalisé
    :rtype: string
    """
    ponctuation = '!@#$%^&*()_-+={}[]:;"\'|<>,.?/~`’'
    for marqueur in ponctuation:
        mot = mot.replace(marqueur, "")
    resultat = mot.lower()
    return resultat


def liste_mots(doc):
    """
    Fonction qui permet d'obtenir une liste de tous les mots employés dans un document
    :param doc: un chemin de fichier
    :return: liste des mots
    :rtype: list
    """
    liste = []
    lignes = doc.xpath('//tei:reg/text()', namespaces=ns)
    for ligne in lignes:
        mots = ligne.split()
        for mot in mots:
            mot = normalisation(mot)
            if mot not in stop_words:
                liste.append(mot)
    return liste


def decompte(liste):
    """
    Fonction qui compte le nombre d'occurrences de chaque mot

    :param liste: liste de mots
    :return: un dictionnaire ayant pour clefs le mot et pour valeur son nombre d'occurrences
    :rtype:dict
    """
    resultats = {}
    for mot in liste:
        if mot not in resultats:
            resultats[mot] = liste.count(mot)
    return resultats


def affichage_auteur(doc):
    """
    Fonction qui permet d'obtenir le nom normalisé de l'auteur à partir du titre du fichier pour en afficher le portrait

    :param doc: un chemin de fichier
    :return: string
    """
    doc = str(doc)
    # re.findall permet de trouver toutes les occurences du motif recherché, on en conserve ainsi que le premier
    nom = re.findall("([A-Za-z]+)", doc)[0]
    return url_for("static",  filename="images/" + nom + ".jpg")
