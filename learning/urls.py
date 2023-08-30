
from learning import views
from django.contrib import admin
from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('', views.index_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact_view, name='contact'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('about/', views.about_view, name="about"),
    path('documents/', views.documents_list_view, name="documents-list"),
    path('document/<str:slug>', views.doc_details_view, name="doc-details"),
    path('account/settings/', views.Settings.as_view(), name='settings'),
    path('account/settings/password-change/', PasswordChangeView.as_view(template_name='learning/password_change.html', success_url=reverse_lazy('password-change-done')), name='password-change'),
    path('account/settings/passord-change-done/', PasswordChangeDoneView.as_view(template_name='learning/password_change_done.html'), name='password-change-done'),

]