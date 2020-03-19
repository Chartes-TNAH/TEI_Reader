# lxml est la librairie permettant de traiter du XML en python
from lxml import etree

# Flask permettra d'afficher les résultats sur une page html
from flask import Flask, render_template

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

def presenter(doc):
    titre = doc.xpath('//tei:titleStmt/tei:title/text()', namespaces=ns)[0]
    auteur = doc.xpath('//tei:titleStmt/tei:author/text()', namespaces=ns)[0]
    editeur = doc.xpath('//tei:titleStmt/tei:editor/text()', namespaces=ns)[0]

    return {
        "Titre": titre,
        "Auteur": auteur,
        "Éditeur": editeur
    }


app = Flask("Application")
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/<document>/Accueil")
def accueil(document):
    doc = etree.parse("data/" + document)
    return render_template("Accueil.html")


@app.route("/<document>/Table_des_matieres")
def table_matieres(document):
    doc = etree.parse("data/" + document)
    return render_template("Table_matieres.html", table=table_des_matieres(doc))

@app.route("/<document>/Index_lieux")
def index_des_lieux(document):
    doc = etree.parse("data/" + document)
    return render_template("Index_lieux.html", index=index_lieux(doc))

@app.route("/<document>/Index_personnages")
def index_des_personnages(document):
    doc = etree.parse("data/" + document)
    return render_template("Index_personnages.html", index=index_personnages(doc))

@app.route("/<document>/Presentation")
def presentation(document):
    doc = etree.parse("data/" + document)
    return render_template("Presentation.html", infos=presenter(doc))

if __name__ == "__main__":
    app.run()
