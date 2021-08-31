from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('shows/new',views.newshow),
    path('shows/create',views.create_newshow),
    path('shows/<id>/',views.showinfo),
    path('shows',views.shows),
    path('shows/<id>/edit',views.edit),
    path('shows/<id>/update',views.update),
    path('shows/<id>/destroy',views.destroy),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
]
