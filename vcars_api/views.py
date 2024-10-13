from rest_framework import generics

from vcars.models import Pic
from vcars_api.serializers import PicSerializer


class GetPicsApiView(generics.ListAPIView):
    queryset = Pic.objects.all()
    serializer_class = PicSerializer