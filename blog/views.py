from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article, Category, Tag, Comment, Favorite, Notification
from .forms import ArticleForm, CommentForm
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article, Category, Tag, Comment, Favorite, Notification
from .forms import ArticleForm, CommentForm
import json

def home(request):
    articles = Article.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()

    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    tag_filter = request.GET.get('tag', '')

    if query:
        articles = articles.filter(title__icontains=query)
    if category_filter:
        articles = articles.filter(category__name=category_filter)
    if tag_filter:
        articles = articles.filter(tags__name=tag_filter)

    unread_notifications = 0
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        articles_data = [{
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'likes_count': article.likes.count(),
            'comments_count': article.comments.count(),
            'liked': request.user.is_authenticated and request.user in article.likes.all()
        } for article in articles]
        return JsonResponse({'articles': articles_data})

    return render(request, 'blog/home.html', {
        'articles': articles,
        'categories': categories,
        'tags': tags,
        'category_filter': category_filter,
        'tag_filter': tag_filter,
        'unread_notifications': unread_notifications,
    })
    
    
def search_suggestions(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        query = request.GET.get('q', '')
        suggestions = Article.objects.filter(title__icontains=query)[:5]
        suggestions_data = [{'title': article.title} for article in suggestions]
        return JsonResponse({'suggestions': suggestions_data})
    return JsonResponse({'suggestions': []})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.views += 1
    article.save()

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        if not request.user.is_authenticated:
            if is_ajax:
                return JsonResponse({'success': False, 'error': 'Utilisateur non connecté'}, status=401)
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            Notification.objects.create(
                user=article.author,
                message=f"{request.user.username} a commenté votre article : {article.title}",
                is_read=False,
                is_displayed=False
            )
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'author': request.user.username,
                    'content': comment.content
                }, status=200)
            messages.success(request, 'Commentaire ajouté !')
            return redirect('article_detail', article_id=article.id)
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'error': 'Formulaire invalide'}, status=400)
            messages.error(request, 'Erreur dans le formulaire.')
    else:
        form = CommentForm()

    unread_notifications = 0
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'form': form,
        'unread_notifications': unread_notifications,
    })
    
    

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()
            messages.success(request, 'Article créé avec succès !')
            return redirect('home')
    else:
        form = ArticleForm()

    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'blog/create_article.html', {
        'form': form,
        'unread_notifications': unread_notifications,
    })
    

@login_required
def like_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST' and is_ajax:
        try:
            # Lire le corps JSON
            data = json.loads(request.body)
            liked = data.get('liked', False)  # Récupérer 'liked' du JSON, défaut à False
            if liked:
                if request.user not in article.likes.all():
                    article.likes.add(request.user)
                    Notification.objects.create(
                        user=article.author,
                        message=f"{request.user.username} a aimé votre article : {article.title}",
                        is_read=False,
                        is_displayed=False
                    )
            else:
                if request.user in article.likes.all():
                    article.likes.remove(request.user)
            return JsonResponse({
                'success': True,
                'like_count': article.likes.count()
            }, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Données JSON invalides'}, status=400)
    return JsonResponse({'success': False, 'error': 'Requête invalide'}, status=400)


@login_required
def favorite_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, article=article)
    if not created:
        favorite.delete()
    return redirect('article_detail', article_id=article.id)


def article_comments(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        comments = article.comments.all()
        comments_data = [{
            'author': comment.author.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for comment in comments]
        return JsonResponse({'comments': comments_data}, status=200)
    return JsonResponse({'error': 'Requête invalide'}, status=400)


@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        content = request.POST.get('content', '').strip()
        if content:
            comment = Comment.objects.create(
                article=article,
                author=request.user,
                content=content
            )
            return JsonResponse({
                'success': True,
                'author': request.user.username,
                'content': content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }, status=200)
        return JsonResponse({'success': False, 'error': 'Le commentaire ne peut pas être vide'}, status=400)
    return JsonResponse({'success': False, 'error': 'Requête invalide'}, status=400)




@login_required
def user_profile(request):
    tab = request.GET.get('tab', 'articles')
    
    # Définir notifications avant toute condition pour éviter UnboundLocalError
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Définir articles en fonction de l'onglet
    if tab == 'likes':
        articles = request.user.liked_articles.all()
    elif tab == 'notifications':
        articles = []  # Pas d'articles dans cet onglet
    else:
        articles = Article.objects.filter(author=request.user)
    
    favorites = Favorite.objects.filter(user=request.user).select_related('article')
    unread_notifications = notifications.filter(is_read=False).count()

    # Pas de mise à jour de is_read ici, cela sera fait au départ via AJAX
    return render(request, 'blog/profile.html', {
        'articles': articles,
        'favorites': favorites,
        'notifications': notifications,
        'tab': tab,
        'unread_notifications': unread_notifications,
    })

@login_required
def mark_notifications_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def check_notifications(request):
    # Récupérer les notifications non lues ET non affichées
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False,
        is_displayed=False
    ).order_by('-created_at')[:5]
    new_notifications = [{'message': notif.message, 'id': notif.id} for notif in notifications]
    
    # Marquer ces notifications comme affichées
    if new_notifications:
        Notification.objects.filter(
            user=request.user,
            id__in=[notif['id'] for notif in new_notifications]
        ).update(is_displayed=True)
    
    return JsonResponse({'new_notifications': new_notifications})


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')