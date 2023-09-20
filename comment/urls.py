from django.urls import path
from . import views

urlpatterns = [
    path('forum/', views.ForumListCreateApiView.as_view()),
    path('news/<int:pk>/', views.ForumUpdateDestroyApiView.as_view()),
    path('forum/<int:forum_id>/comments/', views.comment_list_create_api_view),
    path('forum/<int:forum_id>/comments/<int:comment_id>/', views.comment_retrieve_update_destroy_api_view),

]
