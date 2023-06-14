from django.urls import path
from . import views


urlpatterns=[
    path('signupapi/',views.signup,name='signupapi'),
    path('loginapi/',views.login_user,name='loginapi'),
    path('',views.listmed,name='listmedicineapi'),
    path('logoutapi/',views.logout_user,name='logoutapi'),
    path('addapi/',views.addmed,name='addmedicineapi'),
    path('updateapi/<int:id>',views.updatemed,name='updatemedicineapi'),
    path('deleteapi/<int:id>',views.deletemed,name='deletemedicineapi'),
    path('searchapi/',views.searchmed,name='searchapi'),


]