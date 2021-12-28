# Projet 9 DA-Python OC (Hélène Mignon)

***Livrable du Projet 9 du parcours D-A Python d'OpenClassrooms***

_Testé sous Windows 10 - Python 3.9.5 - Django 3.2.9_

## Initialisation du projet

### Windows :

    git clone https://github.com/hmignon/P9_mignon_helene.git

    cd P9_mignon_helene 
    python -m venv env 
    env\Scripts\activate

    pip install -r requirements.txt


### MacOS et Linux :

    git clone https://github.com/hmignon/P9_mignon_helene.git

    cd P9_mignon_helene 
    python3 -m venv env 
    source env/bin/activate

    pip install -r requirements.txt


## Utilisation

1. Lancer le serveur Django:


    python manage.py runserver


2. Dans le navigateur de votre choix, se rendre à l'adresse http://127.0.0.1:8000/


## Infos

### Django administration

Identifiant : **Admin** | Mot de passe : **litreview**

--> http://127.0.0.1:8000/admin/

### Liste des utilisateurs existants

| *Identifiant* | *Mot de passe* |
|---------------|----------------|
| annaleecall   | password321    |
| Bristlewood   | password321    |
| gardensail03  | password321    |
| KaitReads     | password321    |
| MarbleFox     | password321    |
| QElizabeth    | password321    |
| TestUser      | password321    |


### Fonctionnalités

- Se connecter et s'inscrire ;
- Consulter son profil et le modifier, ajouter une image de profil ;
- Consulter un flux contenant les tickets et critiques des utilisateurs auxquels on est abonné ;
- Créer des tickets de demande de critique ;
- Créer des critiques, en réponse ou non à des tickets ;
- Voir ses propres posts, les modifier ou les supprimer ;
- Suivre d'autres utilisateurs, ou se désabonner.