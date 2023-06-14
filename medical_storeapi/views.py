from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
)
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.shortcuts import render

from medical_store.models import Medicine
from .seriallizer import MedicineSerializer

from medical_store.forms import SignupForm, LoginForm, MedicalEditform, Medicalupdateform


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request):
    registerform = SignupForm(request.data)
    if registerform.is_valid():
        username = registerform.cleaned_data['username']
        email = registerform.cleaned_data['emailid']
        firstname = registerform.cleaned_data['firstname']
        lastname = registerform.cleaned_data['lastname']
        password = registerform.cleaned_data['password']
        if User.objects.filter(username=username).exists():
            registerform = SignupForm(request.POST)
            context = {'registerform': registerform.data,
                       'error': 'Username already exists add a new one'}
            return Response(context, status=HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            first_name=firstname,
                                            last_name=lastname)
            user.save()
            context = {'registerform': registerform.data,
                       'success': 'Created user'}
            return Response(context, status=HTTP_200_OK)
    else:
        registerform = SignupForm(request.POST)
        context = {'registerform': registerform.data,
                   'errors': registerform.errors}
        return Response(context, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_user(request):
    username = None
    password = None
    loginform = LoginForm(request.data)
    if loginform.is_valid():
        username = loginform.cleaned_data['username']
        password = loginform.cleaned_data['password']
        if username is None or password is None:
            return Response({'error': 'Provide Both username and password'},
                            status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credential'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def logout_user(request):
    logout(request)

    return Response({'success': 'logout success'}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def listmed(request):
    medicine = Medicine.objects.all()
    context = MedicineSerializer(medicine, many=True)
    return Response(context.data, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def addmed(request):
    form = MedicalEditform(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            context = {'Medicine add': form.data,
                       'success': 'Medicine Added success'}
            return Response(context, status=HTTP_200_OK)
        else:
            medicalform = MedicalEditform(request.POST)
            context = {'registerform': medicalform.data,
                       'errors': medicalform.errors}
            return Response(context, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def updatemed(request, id):
    data = get_object_or_404(Medicine, id=id)
    form = Medicalupdateform(request.POST, instance=data)
    if request.method == "POST":
        if form.is_valid():

            form.save()
            context = {'Medicine add': form.data,
                       'success': 'Medicine Updated success'}
            return Response(context, status=HTTP_200_OK)
        else:
            medicalform = Medicalupdateform(request.POST)
            context = {'registerform': medicalform.data,
                       'errors': medicalform.errors}
            return Response(context, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["DELETE"])
@permission_classes((IsAuthenticated,))
def deletemed(request, id):

    data = get_object_or_404(Medicine, id=id)
    data.delete()
    return Response({"success": "Medicine deleted success"}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def searchmed(request):
    search = request.query_params.get('search', '')
    if search:
        allMed = Medicine.objects.filter(medicine_name__istartswith=search)
        if not allMed:
            return Response({"No item with your search", search}, status=HTTP_204_NO_CONTENT)

        else:
            
            serializer = MedicineSerializer(allMed, many=True)
            return Response(serializer.data, status=HTTP_200_OK)
