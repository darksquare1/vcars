from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, View
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.cache import cache
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
        queryset = cache.get_or_set('cached_pics_list', super().get_queryset())
        tag_slug = self.kwargs.get('tag_slug', None)
        if tag_slug:
            try:
                tag = get_object_or_404(Tag, slug=tag_slug)
                queryset = queryset.filter(tags__in=[tag])
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
            return render(request, 'includes/comment.html', context={'comment': comment})
        return HttpResponseBadRequest()


class CreatePic(SuccessMessageMixin, CreateView):
    form_class = PicForm
    template_name = 'vcars/post_pic.html'
    success_message = 'Картинка успешно добавлена!'

    def get_success_url(self):
        return reverse_lazy('vcars:pic_detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        cache.delete('cached_pics_list')
        return super().form_valid(form)


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


def custom_404(request, exception):
    return render(request, 'errors/custom_error.html', status=404,
                  context={'error_msg': 'К сожалению данная страница не была найдена'})


def custom_500(request):
    return render(request, 'errors/custom_error.html', status=500,
                  context={'error_msg': 'Внутрення ошибка сервера, мы уже работает над исправлением'})


def custom_403(request, exception):
    return render(request, 'errors/custom_error.html', status=403,
                  context={'error_msg': 'Доступ к этой странице запрещен'})
