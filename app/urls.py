from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('map/', views.map, name='map'),
    path('piechart/', views.ChartAnalysisEndpoint.as_view(), name='piechart'),
    path('worldmap/', views.WorldAnalysisEndpoint.as_view(), name='worldmap'),
]
