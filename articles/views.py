from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Article, Category, Comment, ArticleLike

def article_list(request):
    articles = Article.objects.filter(status='published')
    categories = Category.objects.all()
    featured = Article.objects.filter(status='published', featured=True)[:3]
    
    context = {
        'articles': articles,
        'categories': categories,
        'featured': featured,
        'page_title': 'Articles & Insights',
    }
    return render(request, 'articles/list.html', context)

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    recent = Article.objects.filter(status='published').exclude(id=article.id)[:3]
    comments = article.comments.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('comment', '').strip()
        if content:
            Comment.objects.create(article=article, author=request.user, content=content)
            messages.success(request, 'Comment posted!')
            return redirect('articles:detail', slug=slug)
    
    context = {
        'article': article,
        'recent': recent,
        'comments': comments,
        'page_title': article.title,
    }
    return render(request, 'articles/detail.html', context)

@login_required
def like_article(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    like, created = ArticleLike.objects.get_or_create(article=article, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': article.likes.count()})
@login_required
def edit_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if article.author != request.user.username and not request.user.is_staff:
        messages.error(request, 'You can only edit your own articles.')
        return redirect('articles:detail', slug=slug)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        if title and content:
            article.title = title
            article.content = content
            article.save()
            messages.success(request, 'Article updated!')
            return redirect('articles:detail', slug=article.slug)
    
    context = {'article': article, 'page_title': f'Edit: {article.title}'}
    return render(request, 'articles/edit.html', context)

@login_required
def delete_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if article.author != request.user.username and not request.user.is_staff:
        messages.error(request, 'You can only delete your own articles.')
        return redirect('articles:detail', slug=slug)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted.')
        return redirect('articles:list')
    
    context = {'article': article, 'page_title': 'Delete Article'}
    return render(request, 'articles/delete.html', context)