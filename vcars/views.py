from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, View
from django.http import JsonResponse
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework.reverse import reverse_lazy
from taggit.models import Tag
from vcars.models import Pic, Comment, Rating
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


class CreatePic(SuccessMessageMixin, CreateView):
    form_class = PicForm
    template_name = 'vcars/post_pic.html'
    success_message = 'Картинка успешно добавлена!'

    def get_success_url(self):
        return reverse_lazy('vcars:pic_detail', kwargs={'slug': self.object.slug})


class LikeView(View):
    model = Rating

    def post(self, request, *args, **kwargs):
        pic_id = self.request.POST.get('pic_id')
        val = int(request.POST.get('value'))
        ip = request.META.get('HTTP_X_FORWARDED_FOR') if request.META.get('HTTP_X_FORWARDED_FOR') else request.META.get(
            'REMOTE_ADDR')
        user = request.user if request.user.is_authenticated else None
        rating, created = self.model.objects.get_or_create(
            pic_id=pic_id,
            ip=ip,
            defaults={'rating': val, 'user': user}
        )
        if not created:
            if rating.rating == val:
                rating.delete()
            else:
                rating.rating = val
                rating.user = user
                rating.save()
        return JsonResponse({'rating_sum': rating.pic.count_rating()})

