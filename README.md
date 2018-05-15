Ceci est une application Backend Django (Python).

Installer Python et pip : [https://docs.djangoproject.com/en/2.0/intro/install/](https://docs.djangoproject.com/en/2.0/intro/install/)

Placez-vous à la racine du projet puis lancez la commande suivante : 

`pip install -r /path/to/requirements.txt`

(MODE DEGRADE) Par défaut la base de données SQLLite "us.census.db" est à placer à la racine du projet. Sinon il faudra modifier le fichier `liv_census_test_api/settings.py`pour préciser l'emplacement du fichier de base de données SQLLite (une amélioration consistera à changer plus facilement ce paramétrage à l'aide de mécanisme de gestion des settings ou de variables d'environnement).

Pour lancer l'application il suffit d'exécuter la commande suivante : 

`python manage.py runserver`