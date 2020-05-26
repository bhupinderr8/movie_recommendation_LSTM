from django.db.models import Q
from rest_framework.generics import ListAPIView
# from . import helper
from .models import TitleBasics
from .serializers import TitleSerializer


class TitleAPIView(ListAPIView):
    queryset = TitleBasics.objects.all()[0:10]
    serializer_class = TitleSerializer

    def get_queryset(self):
        title_name = self.request.query_params
        queryset = TitleBasics.objects.all()
        return queryset
