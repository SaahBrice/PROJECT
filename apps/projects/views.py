"""
Projects App Views
Project listing and detail pages.
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Project, ProjectCategory


def project_list(request):
    """List all active projects with filtering"""
    projects = Project.objects.filter(status='active').select_related('category')
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        projects = projects.filter(category__slug=category_slug)
    
    # Filter by status
    status = request.GET.get('status')
    if status == 'urgent':
        projects = projects.filter(is_urgent=True)
    elif status == 'featured':
        projects = projects.filter(is_featured=True)
    
    # Pagination
    paginator = Paginator(projects, 9)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    
    context = {
        'projects': projects,
        'categories': ProjectCategory.objects.all(),
        'current_category': category_slug,
    }
    return render(request, 'projects/list.html', context)


def project_detail(request, slug):
    """Project detail page with needs, updates, and donation options"""
    project = get_object_or_404(
        Project.objects.select_related('category').prefetch_related(
            'needs', 'updates', 'articles', 'testimonials'
        ),
        slug=slug,
        status__in=['active', 'funded', 'completed']
    )
    
    # Get related projects (same category)
    related_projects = Project.objects.filter(
        category=project.category,
        status='active'
    ).exclude(pk=project.pk)[:3]
    
    context = {
        'project': project,
        'needs': project.needs.filter(is_fulfilled=False).order_by('priority'),
        'updates': project.updates.all()[:5],
        'articles': project.articles.filter(status='published')[:3],
        'testimonials': project.testimonials.filter(is_active=True)[:3],
        'related_projects': related_projects,
    }
    return render(request, 'projects/detail.html', context)
