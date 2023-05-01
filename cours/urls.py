
from .import views
from django.urls import path

urlpatterns = [

  	path('cours/', views.cours_view, name='cours'),

#vers l'affichage des leçons d'anglais
    path('english/', views.englishlesson_view, name='english-lessons'),

#vers l'affichage des leçons de math
    path('maths/', views.mathslesson_view, name='maths-lessons'),

    path('geosciences/', views.geosciencelesson_view, name='geoscience-lessons'),

    path('computerscience/', views.cslesson_view, name='cs-lessons'),


#details d'une leçons (anglais, maths, geoscience) urls
    path('cours/english/<str:englesson_slug>/', views.englishlesson_details_view, name='englesson-details'),

    path('cours/maths/<str:mathlesson_slug>/', views.mathslesson_details_view, name='mathslesson-details'),

    path('cours/geosciences/<str:geolesson_slug>/', views.geosciencelesson_details_view, name='geosciencelesson-details'),

    path('cours/computerscience/<str:cslesson_slug>/', views.cslesson_details_view, name='cslesson-details'),


]