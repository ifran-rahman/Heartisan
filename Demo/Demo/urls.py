"""Demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Here we are assigning the path of our url
    path('', views.signIn2,name="signIn2"),
    path('home/', views.home,name="home"),
    path('postsignIn/', views.postsignIn),
    path('DoctorsPostSignIn/', views.DoctorsPostSignIn),
    path('signUp/', views.signUp, name="signup"),
    path('logout/', views.logout, name="log"),
    path('postsignUp/', views.postsignUp),
    path('reset/', views.reset,name="reset"),
    path('postReset/', views.postReset),
    path('graph/',views.line_graph,name='graph'),
    path('doctors_graph/',views.doctors_graph,name='doctors_graph'),
    path('postgraph/', views.postgraph),
    path('graph2/',views.prediction_graph,name='graph2'),
    path('validation/',views.validation,name='validation'),
    path('DoctorsHome/',views.DoctorsHome,name='DoctorsHome'),
    path('doctors_signIn/',views.doctors_signIn,name='doctors_signIn'),
    path('patient_signIn/',views.patient_signIn,name='patient_signIn'),
    path('verify_prediction/',views.verify_prediction,name='verify_prediction')
    
]
