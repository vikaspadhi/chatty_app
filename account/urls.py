from django.urls import path,include
from .views import signin,register , signout
urlpatterns = [
    path('login/', signin),
    path('logout/', signout),
    path('register/', register),
]