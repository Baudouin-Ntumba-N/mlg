
from .import views
from django.urls import path

urlpatterns = [

  	path('cours/', views.cours_view, name='cours'),

#vers l'affichage des leçons d'anglais
    path('cours/english/', views.englishlesson_view, name='english-lessons'),

#vers l'affichage des leçons de math
    path('cours/maths/', views.mathslesson_view, name='maths-lessons'),


#details d'une leçons (anglais, maths, geoscience) urls
    path('cours/english/<str:englesson_slug>/', views.englishlesson_details_view, name='englesson-details'),

    path('cours/maths/<str:mathlesson_slug>/', views.mathslesson_details_view, name='mathslesson-details'),


]