from django_filters.widgets import CSVWidget
from rest_framework import generics

from vcars.models import Pic, Comment
from vcars_api.serializers import PicSerializer, PicWithCommentsSerializer, CommentSerializer
from django_filters import filters, FilterSet


class FilterForPics(FilterSet):
    tags = filters.BaseCSVFilter(
        distinct=True, widget=CSVWidget(), method="filter_tags"
    )
    name = filters.CharFilter()

    class Meta:
        model = Pic
        fields = ['name', 'tags']

    def filter_tags(self, queryset, name, value):
        return queryset.filter(tags__name__in=value)


class GetPicsApiView(generics.ListCreateAPIView):
    queryset = Pic.objects.all()
    serializer_class = PicSerializer
    filterset_class = FilterForPics
    ordering_fields = ('creation_time', 'name')
    search_fields = ('^name',)


class RetrievePicApiView(generics.RetrieveAPIView):
    queryset = Pic.objects.all()
    serializer_class = PicWithCommentsSerializer
    lookup_field = 'slug'


class AddCommentApiView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class AddPicApiView(generics.CreateAPIView):
    queryset = Pic.objects.all()
    serializer_class = PicSerializer

    def perform_create(self, serializer):
        tags_data = serializer.validated_data.get('tags', '')
        if isinstance(tags_data, list):
            tags_data = [tag.strip() for tag in tags_data[0].split(',')]

        serializer.save(tags=tags_data)
