import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2-2C-2023.settings')

import django

django.setup()
from shelves_project.models import Media


def populate():
    media = [{'mediaCode': 'M0001', 'mediaTile': 'Colette'}]


        # make this lol
