from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator
from vcars.models import Pic


def index(request, tag_slug=None):
    pics = Pic.objects.all()
    if tag_slug is not None:
        try:
            tag = get_object_or_404(Tag, slug=tag_slug)
            pics = pics.filter(tags__in=[tag])
        except MultipleObjectsReturned:
            pass
    paginator = Paginator(pics, 6)
    pics = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'vcars/list_pics.html', {'pics': pics})
