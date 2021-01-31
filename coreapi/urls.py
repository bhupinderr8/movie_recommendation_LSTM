from django.urls import path
from . import views


urlpatterns = [
    path('', views.TitleAPIView.as_view(), name='index'),
    path('r/', views.RecommendAPIView.as_view(), name='index'),
]
