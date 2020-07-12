from django.shortcuts import render
from blockchain.forms import *
from blockchain.models import *
from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework.decorators import api_view
from blockchain.serializers import *

import random
import hashlib
import json
import smtplib, ssl
from email.mime.text import MIMEText

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


@api_view(['GET'])
def Register_Code_Gen(request):
    #Required access code and user email in order to generate and send code
    #Generate a 5 character code

    nonce = bytes(random.randrange(1, 100, 1))
    recepient_email = request.data['email']

    h = hashlib.sha256()
    h.update(recepient_email.encode('utf-8'))
    h.update(nonce)

    code = h.hexdigest()[-6: -1]

    rac = Register_Access_Codes.objects.create(code = code, email = recepient_email)

    #Send an email to the patient's email
    port = 465 

    #Must decrypt the password file
    p = open("/var/www/html/blockchain_server/blockchain/Files/email_pswd.bin", "rb")
    key_file = open("/var/www/html/blockchain_server/blockchain/Files/email_pswd_key.bin", "rb")
    key = key_file.read()

    pswd = p.read()

    box = nacl.secret.SecretBox(key)
    pswd = box.decrypt(pswd).decode('utf-8').rstrip()
    
    sender = 'electronichealthchainproject@gmail.com'

    #Put message together
    content = 'Your code is: ' + code
    text_subtype = 'plain'

    msg = MIMEText(content)
    msg['Subject'] = 'Your Registration Code'
    msg['From'] = sender

    #Login to email and send code
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context = context) as server:
        server.login(sender, pswd)
        server.sendmail(sender, recepient_email, msg.as_string())

    #Delete These Variables and Close Files
    p.close()
    key_file.close()

    del box
    del pswd
    del key

    return JsonResponse("Code Successfuly Sent!", safe = False)


@api_view(['POST'])
def Register_User_API(request):
    data = request.data.copy()
    #Get the authcode
    #If the authcode is correct, create the user, then delete the authcode
    authcode = request.data['authcode']
    email = request.data['email']

    real_authcode = Register_Access_Codes.objects.filter(code = authcode, email = email)

    #Checking if authcode is correct
    if(real_authcode.count > 0):
        real_authcode = real_authcode[0]
        if(authcode == real_authcode):
            data.pop('authcode')

            u = User.create_user(**data)

            #Delete the authcode
            real_authcode.delete()

            return JsonResponse("Welcome " + u.username + "!", safe = False)
    else:
        return JsonResponse("Invalid Access Code", safe = False)
    
    return JsonResponse("Something went wrong", safe = False)


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


  

