from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from taggit.models import Tag
from django.core.paginator import Paginator
from vcars.models import Pic, Comment
from vcars.forms import CommentForm, PicForm


def index(request, tag_slug=None):
    query = None
    pics = Pic.objects.all()
    if tag_slug is not None:
        try:
            tag = get_object_or_404(Tag, slug=tag_slug)
            pics = pics.filter(tags__in=[tag])
        except MultipleObjectsReturned:
            pass
    if 'query' in request.GET:
        query = request.GET.get('query')
        search_query = SearchQuery(query)
        search_vector = SearchVector('name', 'body', 'tags')
        pics = pics.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=query)

    paginator = Paginator(pics, 6)
    pics = paginator.get_page(request.GET.get('page', 1))

    return render(request, 'vcars/list_pics.html', {'pics': pics, 'query': query})


def pic_detail(request, pic_id):
    pic = get_object_or_404(Pic, id=pic_id)
    comments = Comment.objects.filter(pic=pic)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.pic = pic
            comment.save()
    else:
        if request.user.is_authenticated:
            form = CommentForm(initial={'name': request.user.username})
        else:
            form = CommentForm()
    return render(request, 'vcars/pic_detail.html', {'pic': pic, 'form': form, 'comments': comments})


def post_pic(request):
    if request.method == 'POST':
        form = PicForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vcars:index')
    else:
        form = PicForm()
    return render(request, 'vcars/post_pic.html', {'form': form})
