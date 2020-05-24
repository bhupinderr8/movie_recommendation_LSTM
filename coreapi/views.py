from rest_framework.generics import ListAPIView
from . import helper
from .models import TitleBasics
from .serializers import TitleBasicsSerializer


class TitleAPIView(ListAPIView):
    queryset = TitleBasics.objects.all()
