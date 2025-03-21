import os
import django
from django.conf import settings

# Configurer l'environnement Django avant tout import de modèles
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()  # Initialise Django avec les settings

# Maintenant, importer les modèles après l'initialisation
from django.contrib.auth.models import User
from blog.models import Category, Tag, Article, Comment, Favorite, Notification

def load_initial_data():
    # Supprimer les données existantes (optionnel)
    User.objects.exclude(username='admin').delete()  # Garde l'utilisateur admin si existant
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Article.objects.all().delete()
    Comment.objects.all().delete()
    Favorite.objects.all().delete()
    Notification.objects.all().delete()

    # Créer des utilisateurs
    user1 = User.objects.create_user(username='alice', password='password123')
    user2 = User.objects.create_user(username='bob', password='password123')
    user3 = User.objects.create_user(username='charlie', password='password123')

    # Créer des catégories
    cat1 = Category.objects.create(name='Technologie')
    cat2 = Category.objects.create(name='Voyage')
    cat3 = Category.objects.create(name='Cuisine')

    # Créer des tags
    tag1 = Tag.objects.create(name='Python')
    tag2 = Tag.objects.create(name='Django')
    tag3 = Tag.objects.create(name='Asie')
    tag4 = Tag.objects.create(name='Recette')

    # Créer des articles
    article1 = Article.objects.create(
        title='Introduction à Django',
        content='Un article sur les bases de Django, un framework Python puissant.',
        author=user1,
        category=cat1,
    )
    article1.tags.add(tag1, tag2)

    article2 = Article.objects.create(
        title='Voyage au Japon',
        content='Récit de mon voyage au Japon avec des photos incroyables.',
        author=user2,
        category=cat2,
    )
    article2.tags.add(tag3)

    article3 = Article.objects.create(
        title='Recette de Sushi',
        content='Apprenez à faire des sushis maison facilement.',
        author=user3,
        category=cat3,
    )
    article3.tags.add(tag4)

    # Ajouter des vues
    article1.views = 50
    article2.views = 30
    article3.views = 20
    article1.save()
    article2.save()
    article3.save()

    # Ajouter des likes
    article1.likes.add(user2, user3)
    article2.likes.add(user1)
    article3.likes.add(user1, user2)

    # Créer des commentaires
    Comment.objects.create(
        article=article1,
        author=user2,
        content='Super article, merci pour les explications !'
    )
    Comment.objects.create(
        article=article2,
        author=user3,
        content='Les photos sont magnifiques !'
    )
    Comment.objects.create(
        article=article3,
        author=user1,
        content='Je vais essayer cette recette ce week-end.'
    )

    # Ajouter des favoris
    Favorite.objects.create(user=user1, article=article2)
    Favorite.objects.create(user=user2, article=article3)
    Favorite.objects.create(user=user3, article=article1)

    # Créer des notifications
    Notification.objects.create(
        user=user1,
        message=f"{user2.username} a aimé votre article : {article1.title}"
    )
    Notification.objects.create(
        user=user2,
        message=f"{user3.username} a commenté votre article : {article2.title}"
    )
    Notification.objects.create(
        user=user3,
        message=f"{user1.username} a ajouté votre article en favoris : {article3.title}"
    )

    print("Données initiales chargées avec succès !")

if __name__ == "__main__":
    load_initial_data()