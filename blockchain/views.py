from django.shortcuts import render
from blockchain.forms import *
from blockchain.models import *

from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework.decorators import api_view
from blockchain.serializers import *


#@api_view(['GET', 'POST',])
def Register_User(request):
    response_message = 'Enter User Data'

    if request.method == 'POST':
        form = Register_Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date_of_birth = form.cleaned_data['date_of_bith']

            user = User.objects.create(username = username, email = email, first_name = first_name, last_name = lastName, date_of_birth = date_of_birth)
            
            user.set_password(password)
            user.save()

            return HttpResponse('<h1>Created a User</h1>')
            response_message = 'Successfuly Registered A User' + str(date_of_birth)


    form = Register_Form()
    return render(request, 'registerForm.html', {'form': form, 'response_message': response_message})

@api_view(['POST'])
def Register_User_API(request):
    serializer = register_user_serializer(data = request.data)
    if(serializer.is_valid()):
        serializer.save()
        return JsonResponse(serializer.data, safe = False)

    return JsonResponse("Failed to create a new user", safe = False)

@api_view(['GET'])
def display_blockchain(request):
    chain = blockchain.objects.all()
    ser = blockchain_serializer(chain, many = True)

    return JsonResponse(ser.data, safe = False)



