"""
Articles App Views
Article listing and detail pages.
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Article, ArticleCategory


def article_list(request):
    """List all published articles with filtering"""
    articles = Article.objects.filter(status='published').select_related('category')
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
    
    # Filter by project
    project_slug = request.GET.get('project')
    if project_slug:
        articles = articles.filter(projects__slug=project_slug)
    
    # Search
    query = request.GET.get('q')
    if query:
        articles = articles.filter(title__icontains=query) | articles.filter(content__icontains=query)
    
    # Pagination
    paginator = Paginator(articles, 12)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    
    context = {
        'articles': articles,
        'categories': ArticleCategory.objects.all(),
        'current_category': category_slug,
        'search_query': query,
    }
    return render(request, 'articles/list.html', context)


def article_detail(request, slug):
    """Article detail page"""
    article = get_object_or_404(
        Article.objects.select_related('category').prefetch_related(
            'projects', 'gallery_images'
        ),
        slug=slug,
        status='published'
    )
    
    # Increment view count
    article.increment_views()
    
    # Get related articles (same category or same projects)
    related_articles = Article.objects.filter(
        status='published'
    ).exclude(pk=article.pk)
    
    if article.category:
        related_articles = related_articles.filter(category=article.category)
    
    related_articles = related_articles[:4]
    
    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'articles/detail.html', context)
