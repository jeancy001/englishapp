from django.shortcuts import render,redirect
from app import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages 
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
import datetime 


# Create your views here.
def home(request): 

  return render (request, "englishroom/home.html")


#Create a register functions 
def register(request): 
  if request.method == "POST":
    username = request.POST['username']
    lastname = request.POST['lastname']
    email    = request.POST['email']
    password = request.POST['password']
    password1 =request.POST['password1']
   
    #add conditions 
    if  User.objects.filter(username = username):
      messages.error(request, "This Username has been taken . ")
      return redirect('englishroom:register')
    
    if User.objects.filter(email = email ):
      messages.error(request, "This email exits already!")
      return redirect("englishroom:register")
    if not "@" in email:
      messages.error(request, "Enter a valid email .")
      return redirect("englishroom:register")
    
    if not username.isalnum(): 
      messages.error(request, "This name is not allowed .")
      return redirect("englishroom:register")
      
    if len(username)<4:
      messages.error(request, "You must shoose a good username .")
      return redirect("englishroom:register")
    if len(lastname)<=3:
      messages.error(request, "Write a correct Last name ")
      return redirect("englishroom:register")
    if User.objects.filter(password = password):
      messages.error(request, "This password is not Strong ,Must container Upper and lowercase ")
      return redirect("englishroom:register")
    if password != password1 :
      messages.error(request, "Password must match .")
      return redirect("englishroom:register")
    if len(password)!= len(password1):
       messages.error(request, "Password must have the same values.")
       return redirect("englishroom:register")
     
  #conditions for gender
    else:
    
      create_user =User.objects.create_user(username,email,password)
      create_user.first_name = username 
      create_user.last_name = lastname
      create_user.save()
      messages.success(request, "Your account has been created successfully.")
      #send mail to the user 
      subject = "English-room"
      #date to be sent
      now = datetime.datetime.now()
      message = f"""
      Hi , {create_user.first_name}\t{create_user.last_name}!\n \n 
      Welcome to {subject}, This web page is all  for you Guy to learn \n 
      and Grow your English Skills  ,by speaking fluently, writting as a native \n 
      and  having  your  Certificate at the end of the courses\n 
      for more Inforamations we wish you to contact us at (+243 84 40 80559)Whatsapp \n 
      or visit our page at www.englishroom.com.
      \n 
      \n 
      author :  @jeancy mpoyi \n 
      Descriptions : Learn English .\n 
      Date : {now.day }-{now.month}-{now.year} \n 
      Time : {now.hour}:{now.minute} :{now.second}
      """ 
      from_to = settings.EMAIL_HOST_USER 
      to_all_users =[create_user.email]
      
      #send email
      send_mail (subject, message, from_to , to_all_users, fail_silently=False)
      
      return redirect ("englishroom:/")

      
  
  return render (request, "englishroom/register.html")


#create a user_login funtions 
def user_login(request): 
  if request.method == "POST":
    username = request.POST["username"]
    password = request.POST["password"]
    if len(username) and len(password) <=0:
      messages.error(request, "Fill out your Username or Password  to continue ")
      return redirect("enlgishroo:user_login")
    user  = authenticate(request,username = username, password =password)
    
    if user is not None :
      login(request, user) 
      username = user.username 
      messages.success(request, "Login successfully !")
      #send message to confirm the user login . 
      
      subject ="Confirm  Login"
      message = f"""
      Hey dear {user.username}! 
      welcome to englishroom  . 
      \n Thank you for your  trust .
      www.engishroom.com
      """
      form_to =settings.EMAIL_HOST_USER 
      to_all_connected = [user.email]
      send_mail (subject,message, form_to, to_all_connected, fail_silently= False )
      return redirect ("englishroom:home")
    else:
      messages.error(request, "Login failed, use a correct ID  ")
      return redirect("englishroom:user_login")
    
  return render (request, "englishroom/user_login.html")





#welcome message for all  users who log in 
def welcome_user(request): 
  
  return render (request, "englishroom/welcome_user.html")

#logout users 
def user_logout(request):
  logout(request)
  return HttpResponseRedirect(reverse("englishroom:user_login"))
