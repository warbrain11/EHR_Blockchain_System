from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
from rest_framework.permissions import IsAuthenticated

from EHR_System.models import *
from EHR_System.serializers import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_patient(request):
    ser = Patient_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Error", safe = False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_emergency_contact(request):
    ser = Emergency_Contacts_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Something went wrong", safe = False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_patient_demographics(request):
    try:
        if(request.data):
            data = {}
            patient = None

            if('ethnicity' in request.data):
                data['ethnicity'] = request.data['ethnicity']
            if('race' in request.data):
                data['race'] = request.data['race']
            if('gender' in request.data):
                data['gender'] = request.data['gender']
            if('sex' in request.data):
                data['sex'] = request.data['sex']
            if('date_of_birth' in request.data):
                data['date_of_birth'] = request.data['date_of_birth']
            if('age' in request.data):
                data['age'] = request.data['age']
            if('height' in request.data):
                data['height'] = request.data['height']
            if('weight' in request.data):
                data['weight'] = request.data['weight']
            if('body_mass_index' in request.data):
                data['body_mass_index'] = request.data['body_mass_index']
            if('primary_language' in request.data):
                data['primary_language'] = request.data['primary_language']
            if('hair_color' in request.data):
                data['hair_color'] = request.data['hair_color']
            if('eye_color' in request.data):
                data['eye_color'] = request.data['eye_color']
            if('dominant_hand' in request.data):
                data['dominant_hand'] = request.data['dominant_hand']
            if('patient_id' not in request.data):
                return JsonResponse("Must include a valid patient ID.", safe = False)

            patient = Patient.objects.get(id = int(request.data['patient_id']))
            demographics = Patient_Demographics.objects.create_demographics(patient = patient, **data)
            ser = Patient_Demographics_Serializer(demographics, many = False)

            return JsonResponse(ser.data, safe = False)

        return JsonResponse("Something went wrong.", safe = False)
    except Patient.DoesNotExist:
        return JsonResponse("Invalid patient ID.", safe = False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_medication(request):
    ser = Medication_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Something went wrong", safe = False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_allergies(request):
    ser = Allergies_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Something went wrong", safe = False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_immunizations(request):
    ser = Immunizations_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Something went wrong", safe = False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_medical_visits(request):
    ser = Medical_Visits_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Something went wrong", safe = False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_surgical_history(request):
    ser = Surgical_History_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Something went wrong", safe = False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_transfusion_history(request):
    ser = History_Of_Transfusions_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Something went wrong", safe = False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_present_illness_history(request):
    ser = History_Of_Present_Illness_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Something went wrong", safe = False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_family_history(request):
    ser = Family_History_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Something went wrong", safe = False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_illness_history(request):
    ser = History_Of_Illnesses_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Something went wrong", safe = False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_disabilities(request):
    ser = Disabilities_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Something went wrong", safe = False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_phys_exam_vitals(request):
    ser = Phys_Exam_Vitals_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Something went wrong", safe = False)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_phys_exam(request):
    ser = Phys_Exam_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Something went wrong", safe = False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_phys_exam_heart(request):
    ser = Phys_Exam_Heart_Serializer(data = request.data)
    if(ser.is_valid()):
        ser.save()
        return JsonResponse(ser.data, safe = False)

    return JsonResponse("Something went wrong", safe = False)

