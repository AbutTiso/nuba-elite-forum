from django.shortcuts import render
from .models import GalleryCategory, GalleryItem

def gallery_list(request):
    categories = GalleryCategory.objects.all()
    items = GalleryItem.objects.all().order_by('-created_at')
    featured = GalleryItem.objects.filter(is_featured=True)[:6]
    
    context = {
        'categories': categories,
        'items': items,
        'featured': featured,
        'page_title': 'Gallery & Media',
    }
    return render(request, 'gallery/list.html', context)
