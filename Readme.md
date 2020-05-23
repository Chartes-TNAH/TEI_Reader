# TEI Reader

Cette application est développée dans le cadre du cours de développement applicatif du master Technologies numériques appliquées à l'histoire (TNAH) de l'École nationale des chartes.

## Fonctionnement
Tei Reader est une application développée en python qui permet de présenter et analyser un corpus d'oeuvres encodées en XML-TEI.
La librairie lxml a été utilisée pour lire les oeuvres.

## Lancement de l'application
Pour lancer cette application, il vous suffit de :
* installer, si ce n'est pas déjà fait `virtualenv` avec `pip install virtualenv` (cette bibliothèque permet de créer des environnements virtuels)
* créer un environnement virtuel avec `virtualenv -p python3 venv`
* activer l'environnement avec `source venv/bin/activate`
* cloner ce *repository*
* vérifier que vous disposez des librairies nécessaires au bon fonctionnement de l'application (Il est possible d'utiliser la commande `pip install -r requirements.txt`)
* lancer le fichier run.py avec la commande :  `python run.py`.

## Lancement des tests unitaires
Pour lancer les tests qui vérifieront le bon fonctionnement des fonctions utilisées par l'application, vous devez, une fois l'environnement virtuel activé, utiliser la commande suivante depuis `application` :
* `python -m unittest tests/test_fonctions.py`

## Crédits
* Les portraits sont issus de [Wikipedia](https://www.wikipedia.org/)
* Les textes sont sous la licence suivante : Attribution 4.0 International (CC BY 4.0).application
Ce corpus a été fourni par [Simon Gabay](https://github.com/gabays), je le remercie tout particulièrement.