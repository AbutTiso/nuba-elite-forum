from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Article, Category, Comment

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
