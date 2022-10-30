from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),
    path('rec/', views.recommend, name='rec'),
    path('getinfo/', views.paging),
    path('search/', views.search),
    path('getDetail/', views.getItemRatingDetail),
    path('like/', views.like),
    path('favorite/', views.favorite),
    path('getFavorite/', views.getFavorite),
]
