#board 서브앱의 urls

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('boardlist/', views.boardlist, name='boardlist'),
    path('logout_action/', views.logout_action, name='logout_action'),
    path('boardlist/board_edit/', views.board_edit, name='board_edit')
]
