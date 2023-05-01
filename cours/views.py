from django.shortcuts import render
from .models import EnglishLesson, MathLesson, Videolesson, GeoscienceLesson, CsLesson
from articles.models import Article
# Create your views here.



def cours_view(request):

  return render(request, 'cours/list.html')

def geosciencelesson_view(request):
  lessons = GeoscienceLesson.objects.all()
  articles = Article.objects.filter(categorie = 3)
  articles = articles.order_by('-id')
  articles = articles[:2]
  videolessons = Videolesson.objects.filter(categorie = 3)
  return render(request, 'cours/geoscience.html', {'lessons':lessons, 'videolessons':videolessons})



def englishlesson_view(request):
  lessons = EnglishLesson.objects.all()
  articles = Article.objects.filter(categorie = 1)
  articles = articles.order_by('-id')
  articles = articles[:2]
  videolessons = Videolesson.objects.filter(categorie = 1)
  return render(request, 'cours/english.html', {'lessons':lessons, 'videolessons':videolessons, 'articles':articles})


def mathslesson_view(request):
  lessons = MathLesson.objects.all()
  articles = Article.objects.filter(categorie = 2)
  articles = articles.order_by('-id')
  articles = articles[:2]
  videolessons = Videolesson.objects.filter(categorie = 2)
  return render(request, 'cours/maths.html', {'lessons':lessons, 'videolessons':videolessons, 'articles':articles})

def cslesson_view(request):
  lessons = CsLesson.objects.all()
  articles = Article.objects.filter(categorie = 4)
  articles = articles.order_by('-id')
  articles = articles[:2]
  videolessons = Videolesson.objects.filter(categorie = 4)
  return render(request, 'cours/cs.html', {'lessons':lessons, 'videolessons':videolessons})

def geosciencelesson_details_view(request, geolesson_slug):
    lessons = GeoscienceLesson.objects.all()
    videolessons = Videolesson.objects.filter(categorie = 3)
    return render(request, 'cours/geoscience.html', {'lessons': lessons, 'videolessons':videolessons})

def englishlesson_details_view(request, englesson_slug):
  lesson_details = EnglishLesson.objects.get(slug=englesson_slug)
  return render(request, 'cours/englishlesson_details.html', {'lesson_details':lesson_details})


def mathslesson_details_view(request, mathlesson_slug):
  lesson_details = MathLesson.objects.get(slug=mathlesson_slug)
  return render(request, 'cours/mathslesson_details.html', {'lesson_details':lesson_details})

def cslesson_details_view(request, cslesson_slug):
  lesson_details = CsLesson.objects.get(slug=cslesson_slug)
  return render(request, 'cours/cslesson_details.html', {'lesson_details':lesson_details})


