# Projet Django Blog avec Bootstrap

Ce projet est une application web permettant aux utilisateurs de créer, consulter et interagir avec des articles de blog. Il inclut des fonctionnalités avancées telles que les catégories, les tags, les likes, les vues, les favoris et les notifications.

## Fonctionnalités Principales

- **Gestion des utilisateurs** : Inscription, connexion et gestion du profil utilisateur.
- **Création et gestion d'articles** : Chaque utilisateur peut créer des articles de blog avec :
  - Une catégorie
  - Des tags
  - Des images, du texte formaté et du contenu enrichi
- **Interactions sociales** :
  - Les utilisateurs peuvent :
    - Liker les articles
    - Commenter les articles
    - Ajouter des articles en favoris
    - Partager les articles sur les réseaux sociaux
- **Notifications** : Les auteurs reçoivent des notifications lorsque leurs articles reçoivent :
  - Des likes
  - Des commentaires
- **Système de filtres** : Possibilité de filtrer les articles par catégorie et/ou tags.
- **Tableaux de bord personnalisés** : Chaque utilisateur a un espace personnel affichant :
  - Ses articles publiés
  - Les articles qu'il a likés
  - Les articles qu'il a ajoutés en favoris

## Prérequis

Avant de commencer, assure-toi d'avoir les outils suivants installés sur ta machine :

- Python 3.x
- Django
- Bootstrap (intégré dans les templates HTML)

## Installation

1. **Cloner le projet**
   ```bash
   git clone https://github.com/votre-utilisateur/votre-repo.git
   cd votre-repo
   ```

2. **Créer et activer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Sur Linux/Mac
   .\venv\Scripts\activate    # Sur Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Appliquer les migrations**
   ```bash
   python manage.py migrate
   ```

5. **Lancer le serveur local**
   ```bash
   python manage.py runserver
   ```

6. **Accéder à l'application**
   Rendez-vous sur [http://localhost:8000](http://localhost:8000)

## Structure du Projet

```
.
├── blog
│   ├── migrations
│   ├── static
│   ├── templates
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── forms.py
├── users
│   ├── templates
│   ├── views.py
│   ├── models.py
│   └── urls.py
├── notifications
│   ├── views.py
│   ├── models.py
│   └── urls.py
├── manage.py
├── db.sqlite3
├── requirements.txt
└── README.md
```

## Modèles Principaux

- **Article** : titre, contenu, catégorie, tags, auteur, date de publication, nombre de vues
- **Commentaire** : contenu, article associé, auteur, date
- **Like** : utilisateur, article associé
- **Favoris** : utilisateur, article associé
- **Notification** : utilisateur cible, message, date de création, état (lu/non lu)

## Instructions pour les Développeurs

- **Créer une nouvelle application**
  ```bash
  python manage.py startapp nom_de_l_application
  ```

- **Créer une migration**
  ```bash
  python manage.py makemigrations
  ```

- **Appliquer les migrations**
  ```bash
  python manage.py migrate
  ```

## Contributions

Les contributions sont les bienvenues ! Merci de respecter les consignes suivantes :
- Fork le dépôt
- Crée une nouvelle branche
- Propose tes changements via une pull request

## Licence

Ce projet est sous licence **MIT**. Voir le fichier `LICENSE` pour plus de détails.

