from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [

    # Chat/Text Messaging Functionality
    path("my-messages/<user_id>/", views.MyInbox.as_view()),
    path("get-messages/<sender_id>/<reciever_id>/", views.GetMessages.as_view()),
    path("send-messages/", views.SendMessages.as_view()),

    # Get profile
    path("profile/<int:pk>/", views.ProfileDetail.as_view()),
    path("search/<username>/", views.SearchUser.as_view()),

]