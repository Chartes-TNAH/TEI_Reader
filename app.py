from lxml import etree
ns = {'tei' : 'http://www.tei-c.org/ns/1.0'}
doc = etree.parse("data/Racine.xml")

auteur = doc.xpath('//tei:author/text()', namespaces=ns)
auteur = auteur[0]
print("L'auteur est " + auteur)

titre = doc.xpath('//tei:title/text()', namespaces=ns)
titre = titre[0]
print("Le titre est " + titre)

perss = doc.xpath('//tei:castItem/text()', namespaces=ns)
for pers in perss :
    print(pers)


