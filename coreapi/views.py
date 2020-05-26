from django.db.models import Q
from rest_framework.generics import ListAPIView
from . import helper
from .models import TitleBasics
from .serializers import TitleSerializer


class TitleAPIView(ListAPIView):
    queryset = TitleBasics.objects.all()
    serializer_class = TitleSerializer

    def get_queryset(self):
        queryset = TitleBasics.objects.all()
        if self.request.GET.get("id"):
            queryset = queryset.filter(
                Q(tconst__exact=self.request.GET.get("id"))
            )
        elif self.request.GET.get("t"):
            queryset = queryset.filter(
                Q(primarytitle__icontains=self.request.GET.get("t")),
                Q(originaltitle__icontains=self.request.GET.get("t"))
            )
        return queryset[0:10]

class RecommendAPIView(ListAPIView):
    queryset = TitleBasics.objects.all()
    serializer_class = TitleSerializer
    def get_queryset(self):
        queryset = TitleBasics.objects.all()
        pref_list = self.request.GET.get("id")
        recommendations = helper.generate_list(pref_list)
        queryset = queryset.filter(
            Q(tconst__in=recommendations)
        )
        return queryset[0:10]
