from lxml import etree
ns = {'tei' : 'http://www.tei-c.org/ns/1.0'}
doc = etree.parse("data/Racine.xml")
'''
auteur = doc.xpath('//tei:author/text()', namespaces=ns)
auteur = auteur[0]
print("L'auteur est " + auteur)

titre = doc.xpath('//tei:title/text()', namespaces=ns)
titre = titre[0]
print("Le titre est " + titre)

perss = doc.xpath('//tei:castItem/text()', namespaces=ns)
for pers in perss :
    print(pers)

perso = doc.xpath('//tei:reg/tei:persName', namespaces=ns)
for persos in perso:
    print(persos.getparent().getparent().getparent().get("n"))'''

#toujours répéter le ns, même à l'intérieur du chemin xpath
#pour avoir les parents : getparent() et les valeurs d'attributs c'est .get

def index_personnages(doc):
    index = {}
    personnages = doc.xpath('//tei:reg/tei:persName', namespaces=ns)
    for personnage in personnages :
        nom = personnage.text
        reg = personnage.getparent()
        choice = reg.getparent()
        ligne = choice.getparent()
        numero_ligne = ligne.get("n")

        if nom not in index :
            index[nom] = []

        index[nom].append(numero_ligne)

    return index

print(index_personnages(doc))

def index_personnages2(doc):
    #fonction qui permet d'avoir un index des personnages (nom + lignes) sous forme de dictionnaire
    index = {}
    lignes = doc.xpath('//tei:body//tei:l[@*]', namespaces=ns)
    #ne prend en compte que les l descendants de body et ayant un attribut
    ligne_precedente = None
    for ligne in lignes:
        if ligne.get("n"):
            numero_de_ligne = ligne.get("n")
        else:
            numero_de_ligne = ligne_precedente

        noms_pers = ligne.xpath('.//tei:reg/tei:persName/text()', namespaces=ns)

        for nom_pers in noms_pers:
            if nom_pers not in index:
                index[nom_pers] = []

            index[nom_pers].append(numero_de_ligne)

        ligne_precedente = numero_de_ligne
    return index
print(index_personnages2(doc))

def index_lieux(doc):
    #fonction qui permet d'avoir un index des lieux (nom + lignes) sous forme de dictionnaire
    index = {}
    lignes = doc.xpath('//tei:body//tei:l[@*]', namespaces=ns)
    #ne prend en compte que les l descendants de body et ayant un attribut
    ligne_precedente = None
    for ligne in lignes:
        if ligne.get("n"):
            numero_de_ligne = ligne.get("n")
        else:
            numero_de_ligne = ligne_precedente

        noms_lieux = ligne.xpath('.//tei:reg/tei:placeName/text()', namespaces=ns)

        for nom_lieu in noms_lieux:
            if nom_lieu not in index:
                index[nom_lieu] = []

            index[nom_lieu].append(numero_de_ligne)

        ligne_precedente = numero_de_ligne
    return index
print(index_lieux(doc))

#Table des matières :

def table_des_matieres(doc):
    index = {}
    divs = doc.xpath('//tei:div', namespaces=ns)

    for div in divs:
        if div.get("type"):
            division = div.get("type")

        titres = div.xpath('.//tei:head', namespaces=ns)

        for titre in titres:
            if titre not in index:
                index[titre] = []
            index[titre].append(division)

    return index
print(table_des_matieres(doc))








