# Flask permettra d'afficher les résultats sur une page html
from flask import Flask
import os

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")

app = Flask(
    "Application",
    template_folder=templates
)

import TEI_Reader.routes

