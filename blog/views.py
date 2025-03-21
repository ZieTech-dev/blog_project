from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article, Category, Tag, Comment, Favorite, Notification
from .forms import ArticleForm, CommentForm
from django.contrib import messages

def home(request):
    articles = Article.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()

    category_filter = request.GET.get('category')
    tag_filter = request.GET.get('tag')
    if category_filter:
        articles = articles.filter(category__name=category_filter)
    if tag_filter:
        articles = articles.filter(tags__name=tag_filter)

    return render(request, 'blog/home.html', {
        'articles': articles,
        'categories': categories,
        'tags': tags,
    })

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            form.save_m2m()  # Sauvegarde les tags
            messages.success(request, 'Article créé avec succès !')
            return redirect('home')
    else:
        form = ArticleForm()
    return render(request, 'blog/create_article.html', {'form': form})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.views += 1
    article.save()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            Notification.objects.create(
                user=article.author,
                message=f"{request.user.username} a commenté votre article : {article.title}"
            )
            messages.success(request, 'Commentaire ajouté !')
            return redirect('article_detail', article_id=article.id)
    else:
        form = CommentForm()

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'form': form,
    })

@login_required
def like_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
        Notification.objects.create(
            user=article.author,
            message=f"{request.user.username} a aimé votre article : {article.title}"
        )
    return redirect('article_detail', article_id=article.id)

@login_required
def favorite_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, article=article)
    if not created:
        favorite.delete()
    return redirect('article_detail', article_id=article.id)

@login_required
def user_profile(request):
    tab = request.GET.get('tab', 'articles')
    if tab == 'likes':
        articles = request.user.liked_articles.all()
    else:
        articles = Article.objects.filter(author=request.user)
    favorites = Favorite.objects.filter(user=request.user).select_related('article')
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'blog/profile.html', {
        'articles': articles,
        'favorites': favorites,
        'notifications': notifications,
        'tab': tab,
    })
    
    
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')