from django.urls import path
from veb_forum.views import author_list_api_view

urlpatterns = [
    path('account/register/', author_list_api_view),
]
