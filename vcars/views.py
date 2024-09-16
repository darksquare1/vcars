from django.views.generic import ListView, DetailView, CreateView

from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework.reverse import reverse_lazy
from taggit.models import Tag
from vcars.models import Pic, Comment
from vcars.forms import CommentForm, PicForm


class PictureListView(ListView):
    model = Pic
    template_name = 'vcars/list_pics.html'
    paginate_by = 6
    context_object_name = 'pics'
    queryset = Pic.custom.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_slug = self.kwargs.get('tag_slug', None)
        if tag_slug:
            try:
                tag = get_object_or_404(Tag, slug=tag_slug)
                queryset = self.model.objects.filter(tags__in=[tag])
            except MultipleObjectsReturned:
                pass
        if 'query' in self.request.GET:
            query = self.request.GET.get('query')
            search_query = SearchQuery(query)
            search_vector = SearchVector('name', 'body', 'tags')
            queryset = queryset.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(
                search=query)
            self.kwargs['query'] = query
        return queryset


class PicDetailView(DetailView):
    model = Pic
    template_name = 'vcars/pic_detail.html'
    context_object_name = 'pic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(pic=self.object)
        return context

    def get(self, request, *args, **kwargs):
        initial = {}
        if request.user.is_authenticated:
            initial = {'name': request.user.username}
        self.extra_context = {'form': CommentForm(initial=initial)}
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pic = self.object
            comment.save()
        self.extra_context = {'form': form}
        return render(request, self.template_name, context=self.get_context_data(**kwargs))


class CreatePic(CreateView):
    form_class = PicForm
    success_url = reverse_lazy('vcars:index')
    template_name = 'vcars/post_pic.html'
