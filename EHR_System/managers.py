from django.db.models import Manager
from django.db import connection
from datetime import datetime
#from EHR_System.models import Patient_Demographics

class Patient_Demographics_Manager(Manager):
    def create_demographics(self, patient, **extra_fields):
        #Calculates Body Mass Index if it is not included so long as height and weight are included
        #----Converts height to meters and weight to kilograms for calculation
        if 'height' in extra_fields and 'weight' in extra_fields and 'body_mass_index' not in extra_fields:
            meter_height = float(extra_fields['height'])/39.37
            kg_weight = float(extra_fields['weight'])/2.205
            body_mass_index = kg_weight/(meter_height * meter_height)

        if 'sex' not in extra_fields:
            raise ValueError("Patient must have a sex")

        if not patient:
            raise ValueError("Could not find patient or patient does not exist")

        if 'date_of_birth' not in extra_fields:
            raise ValueError("Patient must have date of birth")

        if 'age' not in extra_fields and 'date_of_birth' in extra_fields:
            now = datetime.now()
            dob = datetime.strptime(extra_fields['date_of_birth'], "%Y-%m-%dT%H:%M:%S")

            age = int((now - dob).days/365)

        pd = self.create(patient = patient, age = age, body_mass_index = body_mass_index, **extra_fields)
        return pd
        
"""
class Phys_Exam_Manager(Manager):
    def create_phys_exam(self, **extra_fields):
        if 'examining_doctor' not in extra_fields:
            raise ValueError("Examination must have a doctor")
        if 'patient' not in extra_fields:
            raise ValueError("Examination must have a patient")
        if 'date_time' not in extra_fields:
            raise ValueError("Examination must have a date and time")


        #pd = Patient_Demographics.objects.get(patient = patient)
        patient = extra_fields['patient']
        if 'height_in' in extra_fields:
            height = extra_fields['height_in']
            with connection.cursor() as cursor:
                cursor.execute("UPDATE Patient_Demographics SET height = " + str(height) + " WHERE patient_id = " + str(patient) + ";")

        if 'weight_lbs' in extra_fields:
            weight = extra_fields['weight_lbs']
            with connection.cursor() as cursor:
                cursor.execute("UPDATE Patient_Demographics SET weight = " + str(weight) + " WHERE patient_id = " + str(patient) + ";")

        phys_exam = self.create(**extra_fields)
        return phys_exam


#------------------------------------------------
#python manage.py shell test for create_phys_exam
#------------------------------------------------
from EHR_System.models import *
from datetime import datetime
d = datetime.now()
p = Patient.objects.all()[0]
ex_doc = 'Dr.Test Doctor'
ef = {'height_in': 72.0, 'weight_lbs': 175}
pe = Phys_Exam.objects.create_phys_exam(patient = p, date_time = d, examining_doctor = ex_doc, **ef)
"""
