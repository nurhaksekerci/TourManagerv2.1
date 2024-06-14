from django.urls import path
from .views import *

urlpatterns = [
    path('', login, name="loginhome"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('register/', register, name="register"),
    path('pricing/', pricing, name="pricing"),

]
