from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Medicine
from medical_store.forms import LoginForm, MedicalEditform, Medicalupdateform, SignupForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import csv
from datetime import date, timedelta

def signup(request):
    if request.method == "POST":
        regform = SignupForm(request.POST)
        if regform.is_valid():
            firstname = regform.cleaned_data['firstname']
            lastname = regform.cleaned_data['lastname']
            username = regform.cleaned_data['username']
            email = regform.cleaned_data['emailid']
            password = regform.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                regform = SignupForm(request.POST)
                context = {'regform': regform}
                messages.error(request, "User already exists")

                return render(request, 'signup.html', context)
            else:
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password,
                                                first_name=firstname,
                                                last_name=lastname)
                user.save()
                return HttpResponseRedirect(reverse('login'))
        else:
            regform = SignupForm(request.POST)
            context = {'regform': regform}
            return render(request, 'signup.html', context)
    else:
        regform = SignupForm()
    return render(request, 'signup.html', {'regform': regform})


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('listmedicine'))
    else:
        if request.method == 'POST':
            logform = LoginForm(request.POST)
            if logform.is_valid():
                username = logform.cleaned_data['username']
                password = logform.cleaned_data['password']

                user = authenticate(username=username, password=password)

                if user is not None:
                    if user.is_active:
                        login(request,user)
                       
                        return HttpResponseRedirect(reverse('listmedicine'))
                    else:
                        logform = LoginForm(request.POST)
                        messages.error(request,"Check your Credentials")
                        return render(request,"login.html", {"logform": logform})
                else:
                    logform = LoginForm(request.POST)
                    messages.error(request,"Check your Credentials")
                    return render(request, "login.html", {"logform": logform})
            else:
                logform = LoginForm(request.POST)
                messages.error(request,"Check your Credentials")
            
                return render(request, "login.html", {"logform": logform})
        else:
            logform = LoginForm()
    return render(request,'login.html', {"logform": logform})

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def listmed(request):
   medicines=Medicine.objects.all()
   return render(request,'listmedicine.html', {"medicines":medicines})


@login_required(login_url='login')
def addmed(request):
    addform = MedicalEditform (request.POST or None)

    if request.method == "POST":
        if addform.is_valid():
            addform.save()
            return redirect('listmedicine')
    context = {
        "addform": addform
    }
    return render(request, 'addmedicine.html', context)

            
        
    

@login_required(login_url='login')
def updatemed(request,id):
    data = get_object_or_404(Medicine, id=id)
    updateform = Medicalupdateform(instance=data)

    if request.method == "POST":
        updateform = Medicalupdateform(request.POST, instance=data)
        if updateform.is_valid():
            
            updateform.save()
            return redirect('listmedicine')
    context = {
        "updateform": updateform
    }
    return render(request, 'updatemedicine.html', context)
    
    


def deletemed(request,id):
    data=get_object_or_404(Medicine,id=id)
    data.delete()
    return redirect('listmedicine')

def searchmed(request):
    search=request.GET['search']
    medicines= Medicine.objects.filter(medicine_name__istartswith=search).order_by('-medicine_arrived').values()
    return render(request, 'searchmedicine.html',{'medicines':medicines})


from django.db.models import Q
def export_medicine_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="medicine.csv"'
    

    writer = csv.writer(response)
    writer.writerow(['medicine_name','medicine_type', 'price', 'count', 'medicine_arrived', 'medicine_company'])
    writer.writerow([]) 
    current_date = date.today()
    medicines = Medicine.objects.filter(Q(medicine_arrived__year=current_date.year) &
                                    Q(medicine_arrived__month=current_date.month) &
                                    Q(medicine_arrived__day=current_date.day)
).values_list('medicine_name', 'medicine_type', 'price', 'count', 'medicine_arrived', 'medicine_company')
    for medicine in medicines:
        writer.writerow(medicine)

    return response
