from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from EHR_System.models import *
from EHR_System.serializers import *
from blockchain.models import *

"""
Gets for API will display all records in a model if there is no patient id 
specified and if the user (token of the user) sending the request is a super user.

For non super user, test with token c508f934c0afa37ab7c37e299c4b8dc272a394b8
"""

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient(request):
    try:
        #checks to see if request wants to retrieve one patient only by id
        if(request.data):
            data = {}

            if('first_name' in request.data):
                data['first_name'] = request.data['first_name']
            if('last_name' in request.data):
                data['last_name'] = request.data['last_name']
            if('primary_phone' in request.data):
                data['primary_phone'] = request.data['primary_phone']
            if('email' in request.data):
                data['email'] = request.data['email']
            if('cell_phone' in request.data):
                data['cell_phone'] = request.data['cell_phone']

            if('id' in request.data):
                patient_id = int(request.data['id']) 
                patient = Patient.objects.get(id = patient_id)
                ser = Patient_Serializer(patient)

                return JsonResponse(ser.data, safe = False)
            
            patient = Patient.objects.filter(**data)
            if(patient):
                ser = Patient_Serializer(patient, many = True)

                return JsonResponse(ser.data, safe = False)
        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                p = Patient.objects.all()
                ser = Patient_Serializer(p, many = True)
                return JsonResponse(ser.data, safe = False)

        return JsonResponse("Invalid credentials", safe = False)
    except Patient.DoesNotExist:
        return JsonResponse("Patient does not exist with the given id", safe = False)
    except Patient.DoesNotExist:
        return JsonResponse("Invalid Patient ID.", safe = False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_emergency_contact(request):
    try:
        if(request.data):
            data = {}

            if('first_name' in request.data):
                data['first_name'] = request.data['first_name']
            if('last_name' in request.data):
                data['last_name'] = request.data['last_name']
            if('primary_phone' in request.data):
                data['primary_phone'] = request.data['primary_phone']
            if('email' in request.data):
                data['email'] = request.data['email']
            if('relationship_to_patient' in request.data):
                data['relationship_to_patient'] = request.data['relationship_to_patient']

            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                ec = Emergency_Contacts.objects.filter(patient = patient_id, **data)
                ser = Emergency_Contacts_Serializer(ec, many = True)

                return JsonResponse(ser.data, safe = False)
            
            ec = Emergency_Contacts.objects.filter(**data)
            if(ec):
                ser = Emergency_Contacts_Serializer(ec, many = True)

                return JsonResponse(ser.data, safe = False)

        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                ec = Emergency_Contacts.objects.all()
                ser = Emergency_Contacts_Serializer(ec, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No emergency contacts with data given", safe = False)
    except Emergency_Contacts.DoesNotExist:
        return JsonResponse("No emergency contacts with data given", safe = False)
    except Patient.DoesNotExist:
        return JsonResponse("Invalid Patient ID.", safe = False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_patient_demographics(request):
    try:
        if(request.data):
            data = {}

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

            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                demographics = Patient_Demographics.objects.get(patient = patient_id)
                ser = Patient_Demographics_Serializer(demographics, many = False)

                return JsonResponse(ser.data, safe = False)
            
            demographics = Patient_Demographics.objects.filter(**data)
            if(demographics):
                ser = Patient_Demographics_Serializer(demographics, many = True)

                return JsonResponse(ser.data, safe = False)
        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                demographics = Patient_Demographics.objects.all()
                ser = Patient_Demographics_Serializer(demographics, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No patient demographics with data given", safe = False)
    except Patient_Demographics.DoesNotExist:
        return JsonResponse("No patient demographics with data given", safe = False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medication(request):
    try:
        if(request.data):
            data = {}

            if('medication' in request.data):
                data['medication'] = request.data['medication']

            if('frequency_description' in request.data):
                data['frequency_description'] = request.data['frequency_description']

            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                medication = Medication.objects.filter(patient = patient_id)
                ser = Medication_Serializer(medication, many = True)

                return JsonResponse(ser.data, safe = False)
            
            medication = Medication.objects.filter(**data)
            if(medication):
                ser = Medication_Serializer(medication, many = True)

                return JsonResponse(ser.data, safe = False)
        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                medication = Medication.objects.all()
                ser = Medication_Serializer(medication, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No patient medications with data given", safe = False)
    except Medication.DoesNotExist:
        return JsonResponse("No patient medications with data given", safe = False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_allergies(request):
    try:
        if(request.data):
            data = {}

            if('allergic_to' in request.data):
                data['allergic_to'] = request.data['allergic_to']

            if('allergy_notes' in request.data):
                data['allergy_notes'] = request.data['allergy_notes']

            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                allergy = Allergies.objects.filter(patient = patient_id)
                ser = Allergies_Serializer(allergy, many = True)

                return JsonResponse(ser.data, safe = False)

            allergy = Allergies.objects.filter(**data)
            if(allergy):
                ser = Allergies_Serializer(allergy, many = True)

                return JsonResponse(ser.data, safe = False)
        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                allergy = Allergies.objects.all()
                ser = Allergies_Serializer(allergy, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No patient allergies with data given", safe = False)
    except Allergies.DoesNotExist:
        return JsonResponse("No patient allergies with data given", safe = False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_immunizations(request):
    try:
        if(request.data):
            data = {}
         
            if('vaccine' in request.data):
                data['vaccine'] = request.data['vaccine']

            if('date_time' in request.data):
                data['date_time'] = datetime.strptime(request.data['date_time'], "%Y-%m-%dT%H:%M:%S")

            if('complications' in request.data):
                data['complications'] = request.data['complications']

            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                immunization = Immunizations.objects.filter(patient = patient_id)
                ser = Immunizations_Serializer(immunization, many = True)

                return JsonResponse(ser.data, safe = False)

            immunization = Immunizations.objects.filter(**data)
            if(immunization):
                ser = Immunizations_Serializer(immunization, many = True)

                return JsonResponse(ser.data, safe = False)

        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                immunization = Immunizations.objects.all()
                ser = Immunizations_Serializer(immunization, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No patient immunizations with data given", safe = False)
    except Immunizations.DoesNotExist:
        return JsonResponse("No patient immunizations with data given", safe = False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_medical_visits(request):
    try:
        if(request.data):
            data = {}
         
            if('reason' in request.data):
                data['reason'] = request.data['reason']

            if('date_time' in request.data):
                data['date_time'] = datetime.strptime(request.data['date_time'], "%Y-%m-%dT%H:%M:%S")

            if('main_complaint' in request.data):
                data['main_complaint'] = request.data['main_complaint']

            if('description' in request.data):
                data['description'] = request.data['description']

            if('type_of_visit' in request.data):
                data['type_of_visit'] = request.data['type_of_visit']

            if('examining_doctor' in request.data):
                data['examining_doctor'] = request.data['examining_doctor']

            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                visit = Medical_Visits.objects.filter(patient = patient_id)
                ser = Medical_Visits_Serializer(visit, many = True)

                return JsonResponse(ser.data, safe = False)

            visit = Medical_Visits.objects.filter(**data)
            if(visit):
                ser = Medical_Visits_Serializer(visit, many = True)

                return JsonResponse(ser.data, safe = False)

        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                visit = Medical_Visits.objects.all()
                ser = Medical_Visits_Serializer(visit, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No patient medical visits with data given", safe = False)
    except Medical_Visits.DoesNotExist:
        return JsonResponse("No patient medical visits with data given", safe = False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_surgical_history(request):
    try:
        if(request.data):
            data = {}
         
            if('reason' in request.data):
                data['reason'] = request.data['reason']

            if('date_time' in request.data):
                data['date_time'] = datetime.strptime(request.data['date_time'], "%Y-%m-%dT%H:%M:%S")

            if('duration' in request.data):
                data['duration'] = datetime.strptime(request.data['duration'], "%H:%M:%S")

            if('operating_doctors' in request.data):
                data['operating_doctors'] = request.data['operating_doctors']

            if('notes' in request.data):
                data['notes'] = request.data['notes']

            if('outcome' in request.data):
                data['outcome'] = request.data['outcome']

            if('complications' in request.data):
                data['complications'] = request.data['complications']

            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                surgery = Surgical_History.objects.filter(patient = patient_id)
                ser = Surgical_History_Serializer(surgery, many = True)

                return JsonResponse(ser.data, safe = False)

            surgery = Surgical_History.objects.filter(**data)
            if(surgery):
                ser = Surgical_History_Serializer(surgery, many = True)

                return JsonResponse(ser.data, safe = False)

        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                surgery = Surgical_History.objects.all()
                ser = Surgical_History_Serializer(surgery, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No patient surgeries with data given", safe = False)
    except Surgical_History.DoesNotExist:
        return JsonResponse("No patient surgeries with data given", safe = False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transfusion_history(request):
    try:
        if(request.data):
            data = {}
         
            if('reason' in request.data):
                data['reason'] = request.data['reason']

            if('date_time' in request.data):
                data['date_time'] = datetime.strptime(request.data['date_time'], "%Y-%m-%dT%H:%M:%S")

            if('units' in request.data):
                data['units'] = request.data['units']

            if('type_of_transfusion' in request.data):
                data['type_of_transfusion'] = request.data['type_of_transfusion']

            if('veinous_access_device' in request.data):
                data['veinous_access_device'] = datetime.strptime(request.data['veinous_access_device'], "%Y-%m-%dT%H:%M:%S")

            if('infusion_device' in request.data):
                data['infusion_device'] = request.data['infusion_device']

            if('infusion_device_settings' in request.data):
                data['infusion_device_settings'] = request.data['infusion_device_settings']
            
            if('blood_type' in request.data):
                data['blood_type'] = request.data['blood_type']

            if('complications' in request.data):
                data['complications'] = request.data['complications']

            if('notes' in request.data):
                data['notes'] = request.data['notes']

            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                transfusion = History_Of_Transfusions.objects.filter(patient = patient_id)
                ser = History_Of_Transfusions_Serializer(transfusion, many = True)

                return JsonResponse(ser.data, safe = False)

            transfusion = History_Of_Transfusions.objects.filter(**data)
            if(transfusion):
                ser = History_Of_Transfusions_Serializer(transfusion, many = True)

                return JsonResponse(ser.data, safe = False)

        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                transfusion = History_Of_Transfusions.objects.all()
                ser = History_Of_Transfusions_Serializer(transfusion, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No patient transfusions with data given", safe = False)
    except History_Of_Transfusions.DoesNotExist:
        return JsonResponse("No patient transfusions with data given", safe = False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_present_illness_history(request):
    try:
        if(request.data):
            data = {}
         
            if('onset' in request.data):
                data['onset'] = datetime.strptime(request.data['onset'], "%Y-%m-%dT%H:%M:%S")

            if('illness' in request.data):
                data['illness'] = request.data['illness']

            if('body_location' in request.data):
                data['body_location'] = request.data['body_location']

            if('description' in request.data):
                data['description'] = request.data['description']

            if('aggravating_factors' in request.data):
                data['aggravating_factors'] = request.data['aggravating_factors']

            if('alleviating_factors' in request.data):
                data['alleviating_factors'] = request.data['alleviating_factors']
           
            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                hpi = History_Of_Present_Illness.objects.filter(patient = patient_id)
                ser = History_Of_Present_Illness_Serializer(hpi, many = True)

                return JsonResponse(ser.data, safe = False)

            hpi = History_Of_Present_Illness.objects.filter(**data)
            if(hpi):
                ser = History_Of_Present_Illness_Serializer(hpi, many = True)

                return JsonResponse(ser.data, safe = False)

        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                hpi = History_Of_Present_Illness.objects.all()
                ser = History_Of_Present_Illness_Serializer(hpi, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No patient surgeries with data given", safe = False)
    except History_Of_Present_Illness.DoesNotExist:
        return JsonResponse("No patient surgeries with data given", safe = False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_family_history(request):
    try:
        if(request.data):
            data = {}
         
            if('date_of_birth' in request.data):
                data['date_of_birth'] = datetime.strptime(request.data['date_of_birth'], "%Y-%m-%dT%H:%M:%S")

            if('date_of_death' in request.data):
                data['date_of_death'] = datetime.strptime(request.data['date_of_death'], "%Y-%m-%dT%H:%M:%S")

            if('family_first_name' in request.data):
                data['family_first_name'] = request.data['family_first_name']

            if('family_last_name' in request.data):
                data['family_last_name'] = request.data['family_last_name']

            if('relationship_to_patient' in request.data):
                data['relationship_to_patient'] = request.data['relationship_to_patient']

            if('health_status' in request.data):
                data['health_status'] = request.data['health_status']

            if('description_of_illnesses' in request.data):
                data['description_of_illnesses'] = request.data['description_of_illnesses']

            if('cause_of_death' in request.data):
                data['cause_of_death'] = datetime.strptime(request.data['cause_of_death'], "%Y-%m-%dT%H:%M:%S")

            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                history = Family_History.objects.filter(patient = patient_id)
                ser = Family_History_Serializer(history, many = True)

                return JsonResponse(ser.data, safe = False)

            history = Family_History.objects.filter(**data)
            if(history):
                ser = Family_History_Serializer(history, many = True)

                return JsonResponse(ser.data, safe = False)

        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                history = Family_History.objects.all()
                ser = Family_History_Serializer(history, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No patient family history with data given", safe = False)
    except Family_History.DoesNotExist:
        return JsonResponse("No patient family history with data given", safe = False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_illness_history(request):
    try:
        if(request.data):
            data = {}
         
            if('onset_date' in request.data):
                data['onset_date'] = datetime.strptime(request.data['onset_date'], "%Y-%m-%dT%H:%M:%S")
            
            if('date_cured' in request.data):
                data['date_cured'] = datetime.strptime(request.data['date_cured'], "%Y-%m-%dT%H:%M:%S")

            if('illness' in request.data):
                data['illness'] = request.data['illness']

            if('body_location' in request.data):
                data['body_location'] = request.data['body_location']

            if('description' in request.data):
                data['description'] = request.data['description']

            if('aggravating_factors' in request.data):
                data['aggravating_factors'] = request.data['aggravating_factors']

            if('alleviating_factors' in request.data):
                data['alleviating_factors'] = request.data['alleviating_factors']
           
            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                history = History_Of_Illnesses.objects.filter(patient = patient_id)
                ser = History_Of_Illnesses_Serializer(history, many = True)

                return JsonResponse(ser.data, safe = False)

            history = History_Of_Illnesses.objects.filter(**data)
            if(history):
                ser = History_Of_Illnesses_Serializer(history, many = True)

                return JsonResponse(ser.data, safe = False)

        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                history = History_Of_Illnesses.objects.all()
                ser = History_Of_Illnesses_Serializer(history, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No patient illness history with data given", safe = False)
    except History_Of_Present_Illness.DoesNotExist:
        return JsonResponse("No patient illness history with data given", safe = False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_disabilities(request):
    try:
        if(request.data):
            data = {}
         
            if('onset_date' in request.data):
                data['onset_date'] = datetime.strptime(request.data['onset_date'], "%Y-%m-%dT%H:%M:%S")

            if('disability' in request.data):
                data['disability'] = request.data['disability']

            if('body_location' in request.data):
                data['body_location'] = request.data['body_location']

            if('description' in request.data):
                data['description'] = request.data['description']

            if('aggravating_factors' in request.data):
                data['aggravating_factors'] = request.data['aggravating_factors']

            if('alleviating_factors' in request.data):
                data['alleviating_factors'] = request.data['alleviating_factors']
           
            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                disabilities = Disabilities.objects.filter(patient = patient_id)
                ser = Disabilities_Serializer(disabilities, many = True)

                return JsonResponse(ser.data, safe = False)

            disabilities = Disabilities.objects.filter(**data)
            if(disabilities):
                ser = Disabilities_Serializer(disabilities, many = True)

                return JsonResponse(ser.data, safe = False)

        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                disabilities = Disabilities.objects.all()
                ser = Disabilities_Serializer(disabilities, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No patient disabilities with data given", safe = False)
    except History_Of_Present_Illness.DoesNotExist:
        return JsonResponse("No patient disabilities with data given", safe = False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_phys_exam_vitals(request):
    try:
        if(request.data):
            data = {}
         
            if('pressure_right_palpatation' in request.data):
                data['pressure_right_palpatation'] = request.data['pressure_right_palpatation']
            
            if('pressure_left_palpatation' in request.data):
                data['pressure_left_palpatation'] = request.data['pressure_left_palpatation']

            if('pressure_right_auscultation' in request.data):
                data['pressure_right_auscultation'] = request.data['pressure_right_auscultation']

            if('pressure_left_auscultation' in request.data):
                data['pressure_left_auscultation'] = request.data['pressure_left_auscultation']

            if('heart_rate' in request.data):
                data['heart_rate'] = request.data['heart_rate']

            if('respiration_rate' in request.data):
                data['respiration_rate'] = request.data['respiration_rate']

            if('temperature_celcius' in request.data):
                data['temperature_celcius'] = request.data['temperature_celcius']
           
            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                vital = Phys_Exam_Vitals.objects.filter(patient = patient_id)
                ser = Phys_Exam_Vitals_Serializer(vital, many = True)

                return JsonResponse(ser.data, safe = False)

            vital = Phys_Exam_Vitals.objects.filter(**data)
            if(vital):
                ser = Phys_Exam_Vitals_Serializer(vital, many = True)

                return JsonResponse(ser.data, safe = False)

        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                vital = Phys_Exam_Vitals.objects.all()
                ser = Phys_Exam_Vitals_Serializer(vital, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No patient vitals with data given", safe = False)
    except Phys_Exam_Vitals.DoesNotExist:
        return JsonResponse("No patient vitals with data given", safe = False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_phys_exam_heart(request):
    try:
        if(request.data):
            data = {}
         
            if('pmi' in request.data):
                data['pmi'] = request.data['pmi']
            
            if('description' in request.data):
                data['description'] = request.data['description']

            if('r_carotid_pulses_desc' in request.data):
                data['r_carotid_pulses_desc'] = request.data['r_carotid_pulses_desc']

            if('l_carotid_pulses_desc' in request.data):
                data['l_carotid_pulses_desc'] = request.data['l_carotid_pulses_desc']

            if('r_brachial_pulses_desc' in request.data):
                data['r_brachial_pulses_desc'] = request.data['r_brachial_pulses_desc']

            if('l_brachial_pulses_desc' in request.data):
                data['l_brachial_pulses_desc'] = request.data['l_brachial_pulses_desc']

            if('r_radial_pulses_desc' in request.data):
                data['r_radial_pulses_desc'] = request.data['r_radial_pulses_desc']

            if('l_radial_pulses_desc' in request.data):
                data['l_radial_pulses_desc'] = request.data['l_radial_pulses_desc']
            
            if('r_femoral_pulses_desc' in request.data):
                data['r_femoral_pulses_desc'] = request.data['r_femoral_pulses_desc']

            if('l_femoral_pulses_desc' in request.data):
                data['l_femoral_pulses_desc'] = request.data['l_femoral_pulses_desc']

            if('r_dorsalis_pedis_pulses_desc' in request.data):
                data['r_dorsalis_pedis_pulses_desc'] = request.data['r_dorsalis_pedis_pulses_desc']

            if('l_dorsalis_pedis_pulses_desc' in request.data):
                data['l_dorsalis_pedis_pulses_desc'] = request.data['l_dorsalis_pedis_pulses_desc']

            if('r_posterior_tibial_pulses_desc' in request.data):
                data['r_posterior_tibial_pulses_desc'] = request.data['r_posterior_tibial_pulses_desc']

            if('l_posterior_tibial_pulses_desc' in request.data):
                data['l_posterior_tibial_pulses_desc'] = request.data['l_posterior_tibial_pulses_desc']
                       
            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                heart = Phys_Exam_Heart.objects.filter(patient = patient_id)
                ser = Phys_Exam_Heart_Serializer(heart, many = True)

                return JsonResponse(ser.data, safe = False)

            heart = Phys_Exam_Heart.objects.filter(**data)
            if(heart):
                ser = Phys_Exam_Heart_Serializer(heart, many = True)

                return JsonResponse(ser.data, safe = False)

        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                heart = Phys_Exam_Heart_Vitals.objects.all()
                ser = Phys_Exam_Heart_Serializer(heart, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No patient heart description with data given", safe = False)
    except Phys_Exam_Heart.DoesNotExist:
        return JsonResponse("No patient heart description with data given", safe = False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_phys_exam(request):
    try:
        if(request.data):
            data = {}
         
            if('date_time' in request.data):
                data['date_time'] = datetime.strptime(request.data['date_time'], "%Y-%m-%dT%H:%M:%S")
            
            if('examining_doctor' in request.data):
                data['examining_doctor'] = request.data['examining_doctor']

            if('height_in' in request.data):
                data['height_in'] = request.data['height_in']

            if('weight_lbs' in request.data):
                data['weight_lbs'] = request.data['weight_lbs']

            if('vitals' in request.data):
                data['vitals'] = request.data['vitals']

            if('lymph_nodes_desc' in request.data):
                data['lymph_nodes_desc'] = request.data['lymph_nodes_desc']

            if('heart' in request.data):
                data['heart'] = request.data['heart']

            if('abdomen_desc' in request.data):
                data['abdomen_desc'] = request.data['abdomen_desc']
            
            if('extremities_desc' in request.data):
                data['extremities_desc'] = request.data['extremities_desc']

            if('neurological_desc' in request.data):
                data['neurological_desc'] = request.data['neurological_desc']

            if('pelvic_desc' in request.data):
                data['pelvic_desc'] = request.data['pelvic_desc']

            if('genitalia_desc' in request.data):
                data['genitalia_desc'] = request.data['genitalia_desc']

            if('rectal_desc' in request.data):
                data['rectal_desc'] = request.data['rectal_desc']

            if('formulation' in request.data):
                data['formulation'] = request.data['formulation']

            if('impression' in request.data):
                data['impression'] = request.data['impression']

            if('plan' in request.data):
                data['plan'] = request.data['plan']

            if('patient_id' in request.data):
                patient_id = int(request.data['patient_id'])
                exam = Phys_Exam.objects.filter(patient = patient_id)
                ser = Phys_Exam_Serializer(exam, many = True)

                return JsonResponse(ser.data, safe = False)

            exam = Phys_Exam.objects.filter(**data)
            if(exam):
                ser = Phys_Exam_Serializer(exam, many = True)

                return JsonResponse(ser.data, safe = False)

        else:
            authToken = request.headers.get('Authorization')
            user = Token.objects.get(key = authToken[6:]).user

            if(user.is_superuser):
                exam = Phys_Exam.objects.all()
                ser = Phys_Exam_Serializer(exam, many = True)
                return JsonResponse(ser.data, safe = False)
            else:
                return JsonResponse("Invalid credentials", safe = False)

        return JsonResponse("No patient physical exam with data given", safe = False)
    except Phys_Exam.DoesNotExist:
        return JsonResponse("No patient physical exam with data given", safe = False)

def get_medical_record(self, request):
    data = {}


    try:
        if('patient_id' not in request.data):
            return JsonResponse("Must include patient id")

        id = int(request.data['patient_id'])

        patient = Patient.objects.get(id = id)
        emergency_contact = Emergency_Contacts.objects.filter(patient = patient)
        patient_demo = Patient_Demographics.objects.get(patient = patient)
        medication = Medication.objects.filter(patient = patient)
        allergies = Allergies.objects.filter(patient = patient)
        immun = Immunizations.objects.filter(patient = patient)
        visits = Medical_Visits.objects.filter(patient = patient)
        surg_hist = Surgical_History.objects.filter(patient = patient)
        trans_hist = History_Of_Transfusions.objects.filter(patient = patient)
        hpi = History_Of_Present_Illness.objects.filter(patient = patient)
        family_hist = Family_History.objects.filter(patient = patient)
        illness_hist = History_Of_Illnesses.objects.filter(patient = patient)
        disabilities = Disabilities.objects.filter(patient = patient)
        
        phys_exam_vitals = Phys_Exam_Vitals.objects.filter(patient = patient)
        phys_exam_heart = Phys_Exam_Heart.objects.filter(patient = patient)
        phys_exam = Phys_Exam.objects.filter(patient = patient)

        #must createa a dictionary that combines phys_exam with phys_exam_heart and phys_exam_vitals
        #of the same patient id and phys_exam_id

        


    except Patient.DoesNotExist:
        return JsonResponse("Patient does not exist.")
