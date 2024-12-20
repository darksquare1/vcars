from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField
from vcars.models import *


class PicSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    slug = serializers.SlugField(max_length=255, read_only=True)

    class Meta:
        model = Pic
        fields = ('id', 'name', 'tags', 'body', 'pic', 'creation_time', 'slug')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PicWithCommentsSerializer(PicSerializer):
    comments = CommentSerializer(many=True, read_only=True)



    class Meta(PicSerializer.Meta):
        fields = PicSerializer.Meta.fields + ('comments',)
