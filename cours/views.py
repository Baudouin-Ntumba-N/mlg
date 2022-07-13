from django.shortcuts import render
from .models import EnglishLesson, MathLesson, Videolesson, GeoscienceLesson
# Create your views here.

def cours_view(request):

  try:
    my_ss = request.session['my_ss']
  except KeyError:
    my_ss = ''

  return render(request, 'cours/list.html', {'msl':my_ss})


def englishlesson_view(request):
  lessons = EnglishLesson.objects.all()
  videolessons = Videolesson.objects.filter(categorie = 2)
  return render(request, 'cours/english.html', {'lessons':lessons, 'videolessons':videolessons})


def mathslesson_view(request):
  lessons = MathLesson.objects.all()
  videolessons = Videolesson.objects.filter(categorie = 1)
  return render(request, 'cours/maths.html', {'lessons':lessons, 'videolessons':videolessons})

def englishlesson_details_view(request, englesson_slug):
  lesson_details = EnglishLesson.objects.get(slug=englesson_slug)
  return render(request, 'cours/englishlesson_details.html', {'lesson_details':lesson_details})


def mathslesson_details_view(request, mathlesson_slug):
  lesson_details = MathLesson.objects.get(slug=mathlesson_slug)
  return render(request, 'cours/mathslesson_details.html', {'lesson_details':lesson_details})


