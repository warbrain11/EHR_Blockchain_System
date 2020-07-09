from django.shortcuts import render
from blockchain.forms import *
from blockchain.models import *
from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework.decorators import api_view
from blockchain.serializers import *

import hashlib
import json

import nacl, nacl.secret, nacl.utils, nacl.pwhash

@api_view(['GET'])
def Show_Users(request):
    users = User.objects.all()
    ser = User_Serializer(users, many = True)

    return JsonResponse(ser.data, safe = False)

@api_view(['POST'])
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

def validate_blockchain(request):
    """
    data = {}
    bc = blockchain.objects.filter()
    count = bc.count() - 1

    while(count > 0):
        current = bc[count]
        prev = bc[count - 1]

        if(current.PreviousHash != prev.Hash):
            data[str(prev.id)] = 'Tampered'
        else:
            data[str(prev.id)] = 'Untampered'

        count -= 1
    """
    return JsonResponse(blockchain.objects.check_blockchain()[0], safe = False)


def write_blockchain_file(request):
    chain = blockchain.objects.all()
    ser = blockchain_serializer(chain, many = True)
    blockchain_status = blockchain.objects.check_blockchain()[1]

    #If the blockchain is not tampered with, it encrypts the blockchain and writes it to a file that is ready for export
    #If it is tampered with it will return an error message
    if(blockchain_status != "Tampered"):
        file = open("/var/www/html/blockchain_server/blockchain/Files/blockchain.bc", "wb")
        key_file = open("/var/www/html/blockchain_server/blockchain/Files/key_file.bin", "rb")
        key = key_file.read()

        blockchain_string = json.dumps(ser.data).encode('utf-8')

        box = nacl.secret.SecretBox(key)
        encrypted_msg = box.encrypt(blockchain_string)
        file.write(encrypted_msg)

        file.close()
        key_file.close()

        return JsonResponse(str(encrypted_msg), safe = False)
   
    return JsonResponse("Will not export a tampered blockchain", safe = False)

@api_view(['POST'])
def repair_blockchain(request):
    files = request.FILES
    blockchain_file = files['blockchain_file']
    return JsonResponse(blockchain.objects.repair(blockchain_file), safe = False)


  

