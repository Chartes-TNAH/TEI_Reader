import glob
from lxml import etree
import os
from stop_words import get_stop_words
stop_words = get_stop_words('fr')
stop_words.extend(["jai", "d", "", "quil", "cest", "dun", "sil", "quun", "quune", "quon", "dune", "nest", "oui", "non",
                   "lon", "jen"])


# Dès qu'on utilise du XPath, il est nécessaire de préciser le namespace, on le met donc dans une variable
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}


def index_personnages(doc):
    """ Fonction qui permet d'obtenir un index des personnages

    :param doc: un document XML donné en entrée
    :return: un dictionnaire ayant pour clefs les noms de personnages et pour valeurs une liste avec les occurences
    de chaque personnage
    :rtype: dict
    """
    index = {}
    # On ne prend en compte que les l descendants de body et ayant un attribut
    lignes = doc.xpath('//tei:body//tei:l[@*]', namespaces=ns)

    ligne_precedente = None
    for ligne in lignes:
            # Pour chaque ligne dotée d'un attribut 'n', on récupère sa valeur. Ce if est nécessaire puisque certaine
            # ligne, notamment les stichomyties, ont uniquement un attribut 'part' : on récupère donc le numéro de
            # la ligne précédente.
        if ligne.get("n"):
            numero_de_ligne = ligne.get("n")
        else:
            numero_de_ligne = ligne_precedente

        noms_pers = ligne.xpath('.//tei:reg/tei:persName/text()', namespaces=ns)

        # On récupère ensuite pour chacune de ses lignes le nom du personnage associé, via l'élément 'persName'
        for nom_pers in noms_pers:
            if nom_pers not in index:
                index[nom_pers] = []

            index[nom_pers].append(numero_de_ligne)

        ligne_precedente = numero_de_ligne
    return index


def index_lieux(doc):
    """ Fonction qui permet d'obtenir un index des lieux

       :param doc: un document XML donné en entrée
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
            if nom_lieu not in index:
                index[nom_lieu] = []

            index[nom_lieu].append(numero_de_ligne)

        ligne_precedente = numero_de_ligne
    return index


def table_des_matieres(doc):
    """ Fonction qui permet d'obtenir une table des matières de chaque document

       :param doc: un document XML donné en entrée
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
        # On récupère tous les speaker puis on utilise le type set() pour n'en garder qu'un. Cette méthode m'a paru
        # être la meilleure puisque lorsque la scène est un monologue, il n'y a pas d'éléments 'stage' or l'élément
        # 'speaker' est présent quel que soit le nombre de personnage(s).
        for scene in scenes:
            titre_scene = scene.xpath('./tei:head/text()', namespaces=ns)[0]
            speaker = set(scene.xpath('.//tei:speaker/text()', namespaces=ns))

            # Pour chaque scène, on stocke dans un dictionnaire le titre (clef 1) et les personnages (clef 2).
            tdm_scene.append({
                "Titre": titre_scene,
                "Personnages": speaker
            })

        # Pour chaque acte, on stocke dans un dictionnaire le titre (clef 1) et la liste des scènes précedemment
        # constituée
        tdm.append({
            "Titre": titre_acte,
            "Scènes": tdm_scene
        })

    return tdm

def remove_element(el):
    """
    Fonction qui permet de supprimer un élément dans l'arbre XML sans supprimer pour autant le texte qui suit
    :param el: un élément xml
    """
    parent = el.getparent()
    if el.tail and el.tail.strip():
        prev = el.getprevious()
        if prev:
            prev.tail = (prev.tail or '') + el.tail
        else:
            parent.text = (parent.text or '') + el.tail
    parent.remove(el)

def presenter(doc):
    titre = doc.xpath('//tei:titleStmt/tei:title/text()', namespaces=ns)[0]
    auteur = doc.xpath('//tei:titleStmt/tei:author/text()', namespaces=ns)[0]
    editeur = doc.xpath('//tei:titleStmt/tei:editor/text()', namespaces=ns)[0]
    date = doc.xpath('//tei:sourceDesc//tei:date/text()', namespaces=ns)[0]
    ville = doc.xpath('//tei:sourceDesc//tei:pubPlace/text()', namespaces=ns)[0]
    editeur_papier = doc.xpath('//tei:sourceDesc//tei:publisher/text()', namespaces=ns)[0]

    lignes = doc.xpath('//tei:l[@n]', namespaces=ns)
    derniere_ligne = lignes[-1]
    derniere_ligne = derniere_ligne.get("n")

    lb = doc.xpath('//tei:castItem//tei:lb', namespaces=ns)

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

def ouvrir_doc(document):
    chemin_actuel = os.path.dirname(os.path.abspath(__file__))
    return etree.parse(os.path.join(chemin_actuel, "data", document))

def corpus():
    files = glob.glob("TEI_Reader/data/*")
    files.sort()
    liste_titre = []
    for file in files:
        file = file.replace("TEI_Reader/data/", "")
        doc = ouvrir_doc(file)
        titre = doc.xpath('//tei:titleStmt/tei:title/text()', namespaces=ns)[0]
        auteur = doc.xpath('//tei:titleStmt/tei:author/text()', namespaces=ns)[0]
        liste_titre.append({
            "Fichier":file,
            "Titre": titre,
            "Auteur": auteur
        })
    return liste_titre

#Fonctions servant à l'analyse du texte

def normalisation(mot):
    ponctuation = '!@#$%^&*()_-+={}[]:;"\'|<>,.?/~`’'
    for marqueur in ponctuation:
        mot = mot.replace(marqueur, "")
    resultat = mot.lower()
    return resultat

def liste_mots(doc):
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
    resultats = {}
    for mot in liste:
        if mot not in resultats:
            resultats[mot] = liste.count(mot)
    return resultats


