from django.db.models import Manager



class Patient_Demographics_Manager(Manager):
    def create_demographics(self, patient, sex, date_of_birth, **extra_fields):
        #Calculates Body Mass Index if it is not included so long as height and weight are included
        #----Converts height to meters and weight to kilograms for calculation
        if 'height' in extra_fields and 'weight' in extra_fields and 'body_mass_index' not in extra_fields:
            meter_height = float(extra_fields['height'])/39.37
            kg_weight = float(extra_fields['weight'])/2.205
            body_mass_index = kg_weight/(meter_height * meter_height)

        if not sex:
            raise ValueError("Patient must have a sex")
        if not patient:
            raise ValueError("Could not find patient or patient does not exist")
        if not date_of_birth:
            raise ValueError("Patient must have date of birth")
        if not patient:
            raise ValueError("Demographics must be associated with a patient")

        pd = self.create(patient = patient, sex = sex, date_of_birth = date_of_birth, body_mass_index = body_mass_index, **extra_fields)
        return pd

# p = Patient.objects.get(first_name = 'Brandon')
# from EHR_System.models import *
# from datetime import datetime
# pd=Patient_Demographics.objects.create_demographics(patient = p, sex = 'male', date_of_birth = dob, height = 71, weight = 170)
# dob = datetime.strptime('1998-08-06', '%Y-%m-%d').date()

        
