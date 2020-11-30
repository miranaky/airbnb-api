from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("", views.UserView.as_view()),
    path("token/", views.login),
    path("me/", views.MeView.as_view()),
    path("me/favs/", views.FavViews.as_view()),
    path("<int:pk>/", views.user_detail),
]
