from django.urls import path 

from . import views 

#app name 
app_name = "englishroom"
urlpatterns = [
  path("",views.welcome_user, name ="welcome_user"),
  path("home",views.home, name ="home"),
  path("register/",views.register, name ="register"),
  path("user_login/",views.user_login, name ="user_login"),
  
  
  
]
