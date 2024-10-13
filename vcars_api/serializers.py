from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField
from vcars.models import *


class PicSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Pic
        fields = '__all__'
