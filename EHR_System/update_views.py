from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from blockchain.models import *
from EHR_System.models import *
from EHR_System.serializers import *
from django.db.models import signals

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_patient(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = Patient._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    old_patient = Patient.objects.filter(id = id)
    block_data['old_data'] = Patient_Serializer(old_patient[0]).data

    #Update the object
    Patient.objects.filter(id = id).update(**data)
    new_patient = Patient.objects.get(id = id)
    block_data['updated_data'] = Patient_Serializer(new_patient).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_emergency_contacts(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = Emergency_Contacts._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    emergency_contacts = Emergency_Contacts.objects.filter(id = id)
    block_data['old_data'] = Emergency_Contacts_Serializer(emergency_contacts[0]).data

    #Update the object
    Emergency_Contacts.objects.filter(id = id).update(**data)
    new_emergency_contacts = Emergency_Contacts.objects.get(id = id)
    block_data['updated_data'] = Emergency_Contacts_Serializer(new_emergency_contacts).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_patient_demographics(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = Patient_Demographics._meta.db_table  

    if('patient' not in data):
        return JsonResponse("Must include patient in request data.", safe = False)

    patient = data.pop('patient')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    demographics = Patient_Demographics.objects.filter(patient = patient)
    block_data['old_data'] = Patient_Demographics_Serializer(demographics[0]).data

    #Update the object
    Patient_Demographics.objects.filter(patient = patient).update(**data)
    new_demographics = Patient_Demographics.objects.get(patient = patient)
    block_data['updated_data'] = Patient_Demographics_Serializer(new_demographics).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)   

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_medication(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = Patient_Demographics._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    medication = Medication.objects.filter(id = id)
    block_data['old_data'] = Medication_Serializer(medication[0]).data

    #Update the object
    Medication.objects.filter(id = id).update(**data)
    new_medication = Medication.objects.get(id = id)
    block_data['updated_data'] = Medication_Serializer(new_medication).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_allergies(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = Patient_Demographics._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    allergies = Allergies.objects.filter(id = id)
    block_data['old_data'] = Allergies_Serializer(allergies[0]).data

    #Update the object
    Allergies.objects.filter(id = id).update(**data)
    new_allergies = Allergies.objects.get(id = id)
    block_data['updated_data'] = Allergies_Serializer(new_allergies).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_immunizations(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = Immunizations._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    immun = Immunizations.objects.filter(id = id)
    block_data['old_data'] = Immunizations_Serializer(immun[0]).data

    #Update the object
    Immunizations.objects.filter(id = id).update(**data)
    new_immun = Immunizations.objects.get(id = id)
    block_data['updated_data'] = Immunizations_Serializer(new_immun).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_medical_visits(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = Medical_Visits._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    visit = Medical_Visits.objects.filter(id = id)
    block_data['old_data'] = Medical_Visits_Serializer(visit[0]).data

    #Update the object
    Medical_Visits.objects.filter(id = id).update(**data)
    new_visit = Medical_Visits.objects.get(id = id)
    block_data['updated_data'] = Medical_Visits_Serializer(new_visit).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_surgical_history(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = Surgical_History._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    surg = Surgical_History.objects.filter(id = id)
    block_data['old_data'] = Surgical_History_Serializer(surg[0]).data

    #Update the object
    Surgical_History.objects.filter(id = id).update(**data)
    new_surg = Surgical_History.objects.get(id = id)
    block_data['updated_data'] = Surgical_History_Serializer(new_surg).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_history_of_transfusions(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = History_Of_Transfusions._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    hot = History_Of_Transfusions.objects.filter(id = id)
    block_data['old_data'] = History_Of_Transfusions_Serializer(hot[0]).data

    #Update the object
    History_Of_Transfusions.objects.filter(id = id).update(**data)
    new_hot = History_Of_Transfusions.objects.get(id = id)
    block_data['updated_data'] = History_Of_Transfusions_Serializer(new_hot).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_history_of_present_illness(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = History_Of_Present_Illness._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    hpi = History_Of_Present_Illness.objects.filter(id = id)
    block_data['old_data'] = History_Of_Present_Illness_Serializer(hpi[0]).data

    #Update the object
    History_Of_Present_Illness.objects.filter(id = id).update(**data)
    new_hpi = History_Of_Present_Illness.objects.get(id = id)
    block_data['updated_data'] = History_Of_Present_Illness_Serializer(new_hpi).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_family_history(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = Family_History._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    family_history = Family_History.objects.filter(id = id)
    block_data['old_data'] = Family_History_Serializer(family_history[0]).data

    #Update the object
    Family_History.objects.filter(id = id).update(**data)
    new_family_history = Family_History.objects.get(id = id)
    block_data['updated_data'] = Family_History_Serializer(new_family_history).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_history_of_illnesses(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = History_Of_Illnesses._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    hoi = History_Of_Illnesses.objects.filter(id = id)
    block_data['old_data'] = History_Of_Illnesses_Serializer(hoi[0]).data

    #Update the object
    History_Of_Illnesses.objects.filter(id = id).update(**data)
    new_hoi = History_Of_Illnesses.objects.get(id = id)
    block_data['updated_data'] = History_Of_Illnesses_Serializer(new_hoi).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_disabilities(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = Disabilities._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    disability = Disabilities.objects.filter(id = id)
    block_data['old_data'] = Disabilities_Serializer(disability[0]).data

    #Update the object
    Disabilities.objects.filter(id = id).update(**data)
    new_disability = Disabilities.objects.get(id = id)
    block_data['updated_data'] = Disabilities_Serializer(new_disability).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_phys_exam_vitals(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = Phys_Exam_Vitals._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    vitals = Phys_Exam_Vitals.objects.filter(id = id)
    block_data['old_data'] = Phys_Exam_Vitals_Serializer(vitals[0]).data

    #Update the object
    Phys_Exam_Vitals.objects.filter(id = id).update(**data)
    new_vitals = Phys_Exam_Vitals.objects.get(id = id)
    block_data['updated_data'] = Phys_Exam_Vitals_Serializer(new_vitals).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_phys_exam_heart(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = Phys_Exam_Heart._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    heart = Phys_Exam_Heart.objects.filter(id = id)
    block_data['old_data'] = Phys_Exam_Heart_Serializer(heart[0]).data

    #Update the object
    Phys_Exam_Heart.objects.filter(id = id).update(**data)
    new_heart = Phys_Exam_Heart.objects.get(id = id)
    block_data['updated_data'] = Phys_Exam_Heart_Serializer(new_heart).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_phys_exam(request):
    data = dict(request.POST.copy())
    #data._mutable = True
    block_data = {}
    block_data['db_op'] = 'Update'  
    block_data['table'] = Phys_Exam._meta.db_table  

    if('id' not in data):
        return JsonResponse("Must include id in request data.", safe = False)

    id = data.pop('id')[0]
    #Fix the request dictionary
    for key in data:
        data[key] = data[key][0]

    #Get the current instance of the object that needs to be updated
    exam = Phys_Exam.objects.filter(id = id)
    block_data['old_data'] = Phys_Exam_Serializer(exam[0]).data

    #Update the object
    Phys_Exam.objects.filter(id = id).update(**data)
    new_exam = Phys_Exam.objects.get(id = id)
    block_data['updated_data'] = Phys_Exam_Serializer(new_exam).data

    #Add the data modification to the blockchain
    new_block = json.dumps(block_data)
    blockchain.objects.add_block(new_block)

    return JsonResponse(block_data) 