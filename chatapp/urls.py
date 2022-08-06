from django.urls import path,include
from .views import index , loadchat ,getroom
urlpatterns = [
    path('', index),
    path('loadchat/<int:receiver>/',loadchat),
    path('getroom/<int:number>/',getroom),
]