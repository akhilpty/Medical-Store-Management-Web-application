
from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('',views.listmed,name='listmedicine'),
    path('add/',views.addmed,name='addmedicine'),
    path('update/<int:id>',views.updatemed,name='updatemedicine'),
    path('delete/<int:id>',views.deletemed,name='deletemedicine'),
    path('search/',views.searchmed,name='search'),
    path('downloadreport/',views.export_medicine_csv,name='downloadreport'),
]
