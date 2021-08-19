from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('shows/new',views.newshow),
    path('shows/create',views.create_newshow),
    path('shows/<id>/',views.showinfo),
    path('shows',views.shows)
]
