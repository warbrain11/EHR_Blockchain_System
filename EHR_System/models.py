from django.db import models
from datetime import datetime
from django.utils import timezone
from rest_framework.authtoken.models import Token
from EHR_System.managers import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from blockchain_server import settings

class Patient(models.Model):
    first_name                      = models.CharField(max_length = 36, blank = False, null = False)
    last_name                       = models.CharField(max_length = 36, blank = False, null = False)
    primary_phone                   = models.CharField(max_length = 10, blank = False, null = False)
    cell_phone                      = models.CharField(max_length = 10, blank = False, null = False)
    email                           = models.EmailField(blank = False, null = False)

class Emergency_Contacts(models.Model):
    patient                         = models.ForeignKey(Patient, on_delete = models.CASCADE)
    first_name                      = models.CharField(max_length = 36, blank = False, null = False)
    last_name                       = models.CharField(max_length = 36, blank = False, null = False)
    primary_phone                   = models.CharField(max_length = 10, blank = False, null = False)
    email                           = models.EmailField(blank = True, null = False)
    relationship_to_patient         = models.CharField(max_length = 26, blank = False, null = False)
    
class Patient_Demographics(models.Model):
    patient                         = models.OneToOneField(Patient, on_delete = models.CASCADE, primary_key = True)
    ethnicity                       = models.CharField(max_length = 36, blank = True, null = False)
    race                            = models.CharField(max_length = 36, blank = True, null = False)
    gender                          = models.CharField(max_length = 36, blank = True, null = False)
    sex                             = models.CharField(max_length = 36, blank = False, null = False)
    date_of_birth                   = models.DateField(blank = False, null = False, default = timezone.now)
    age                             = models.IntegerField(null = False, default = 0)
    height                          = models.IntegerField(null = True)                  #Default in inches
    weight                          = models.IntegerField(null = False, default = 0)    #Default in pounds
    body_mass_index                 = models.DecimalField(max_digits = 6, decimal_places = 3)
    primary_language                = models.CharField(max_length = 36, blank = True)
    hair_color                      = models.CharField(max_length = 36, blank = True)
    eye_color                       = models.CharField(max_length = 36, blank = True)
    dominant_hand                   = models.CharField(max_length = 36, blank = True)

    objects                         = Patient_Demographics_Manager()

class Medication(models.Model):
    patient                         = models.ForeignKey(Patient, on_delete = models.CASCADE)
    medication                      = models.CharField(max_length = 75, blank = False, null = False)
    frequency_description           = models.CharField(max_length = 120, blank = False, null = False)

class Allergies(models.Model):
    patient                         = models.ForeignKey(Patient, on_delete = models.CASCADE)
    allergic_to                     = models.CharField(max_length = 50, null = False, blank = False)
    allergy_notes                   = models.TextField(null = True, blank = True)

class Immunizations(models.Model):
    patient                         = models.ForeignKey(Patient, on_delete = models.CASCADE)
    vaccine                         = models.CharField(max_length = 50, null = False, blank = False)
    date_time                       = models.DateTimeField(null = False, blank = False)
    complications                   = models.TextField(null = False, blank = True, default = 'No Complications')

class Medical_Visits(models.Model):
    patient                         = models.ForeignKey(Patient, on_delete = models.CASCADE)
    reason                          = models.CharField(max_length = 120, null = False, blank = False)
    main_complaint                  = models.TextField(null = False, blank = False)
    description                     = models.TextField(null = False, blank = True)
    type_of_visit                   = models.CharField(max_length = 75, blank = False, null = False)
    examining_doctor                = models.CharField(max_length = 75, blank = False, null = False)
    date_time                       = models.DateTimeField(null = False, blank = False)

class Surgical_History(models.Model):
    patient                         = models.ForeignKey(Patient, on_delete = models.CASCADE)
    date_time                       = models.DateTimeField(null = False, blank = False)
    duration                        = models.TimeField(null = False, blank = False)
    operating_doctors               = models.TextField(null = False, blank = True)
    reason                          = models.TextField(null = False, blank = False)
    notes                           = models.TextField(null = False, blank = False)
    outcome                         = models.TextField(null = False, blank = False)
    complications                   = models.TextField(null = False, blank = False)

class History_Of_Transfusions(models.Model):
    date_time                       = models.DateTimeField(null = False, blank = False)
    patient                         = models.ForeignKey(Patient, on_delete = models.CASCADE)
    units                           = models.DecimalField(max_digits = 6, decimal_places = 3)
    type_of_transfusion             = models.CharField(max_length = 75, blank = False, null = False)
    veinous_access_device           = models.CharField(max_length = 75, blank = True, null = False)
    infusion_device                 = models.CharField(max_length = 75, blank = True, null = False)
    infusion_device_settings        = models.TextField(blank = True, null = False)
    blood_type                      = models.CharField(max_length = 3, blank = False, null = False)
    complications                   = models.TextField(blank = True, null = False, default = "No Complications")
    notes                           = models.TextField(blank = True, null = False)

class History_Of_Present_Illness(models.Model):
    patient                         = models.ForeignKey(Patient, on_delete = models.CASCADE)
    onset                           = models.DateTimeField(null = False, blank = False)
    illness                         = models.CharField(max_length = 75, blank = False, null = False)
    body_location                   = models.CharField(max_length = 135, blank = False, null = False)
    description                     = models.TextField(blank = True, null = False)
    aggravating_factors             = models.TextField(blank = True, null = False)
    alleviating_factors             = models.TextField(blank = True, null = False)

class Family_History(models.Model):
    patient                         = models.ForeignKey(Patient, on_delete = models.CASCADE)
    family_first_name               = models.CharField(max_length = 36, blank = False, null = False)
    family_last_name                = models.CharField(max_length = 36, blank = False, null = False)
    relationship_to_patient         = models.CharField(max_length = 26, blank = False, null = False)
    health_status                   = models.CharField(max_length = 75, blank = True, null = False)
    date_of_birth                   = models.DateField(blank = True, null = False)
    date_of_death                   = models.DateField(blank = True, null = False)
    cause_of_death                  = models.TextField(blank = True, null = False)
    description_of_illnesses        = models.TextField(blank = True, null = False)

class History_Of_Illnesses(models.Model):
    patient                         = models.ForeignKey(Patient, on_delete = models.CASCADE)
    onset_date                      = models.DateTimeField(null = False, blank = False)
    date_cured                      = models.DateTimeField(null = True, blank = True)
    illness                         = models.CharField(max_length = 75, blank = False, null = False)
    body_location                   = models.CharField(max_length = 135, blank = False, null = False)
    description                     = models.TextField(blank = True, null = False)
    aggravating_factors             = models.TextField(blank = True, null = False)
    alleviating_factors             = models.TextField(blank = True, null = False)

class Disabilities(models.Model):
    patient                         = models.ForeignKey(Patient, on_delete = models.CASCADE)
    onset_date                      = models.DateTimeField(null = False, blank = False)
    disability                      = models.CharField(max_length = 75, blank = False, null = False)
    description                     = models.TextField(blank = True, null = False)
    aggravating_factors             = models.TextField(blank = True, null = False)
    alleviating_factors             = models.TextField(blank = True, null = False)

class Phys_Exam_Vitals(models.Model):
    pressure_right_palpatation      = models.CharField(max_length = 12, blank = True, null = False)
    pressure_left_palpatation       = models.CharField(max_length = 12, blank = True, null = False)
    pressure_right_auscultation     = models.CharField(max_length = 12, blank = True, null = False)
    pressure_left_auscultation      = models.CharField(max_length = 12, blank = True, null = False)
    heart_rate                      = models.IntegerField(null = True)
    respiration_rate                = models.IntegerField(null = True)
    temperature_celcius             = models.DecimalField(max_digits = 5, decimal_places = 2)

class Phys_Exam_Heart(models.Model):
    pmi                             = models.CharField(max_length = 50, blank = True)
    description                     = models.TextField(blank = True)
    r_carotid_pulses_desc           = models.CharField(max_length = 200, blank = True)
    l_carotid_pulses_desc           = models.CharField(max_length = 200, blank = True)
    r_brachial_pulses_desc          = models.CharField(max_length = 200, blank = True)
    l_brachial_pulses_desc          = models.CharField(max_length = 200, blank = True)
    r_radial_pulses_desc            = models.CharField(max_length = 200, blank = True)
    l_radial_pulses_desc            = models.CharField(max_length = 200, blank = True)
    r_femoral_pulses_desc           = models.CharField(max_length = 200, blank = True)
    l_femoral_pulses_desc           = models.CharField(max_length = 200, blank = True)
    r_dorsalis_pedis_pulses_desc    = models.CharField(max_length = 200, blank = True)
    l_dorsalis_pedis_pulses_desc    = models.CharField(max_length = 200, blank = True)
    r_posterior_tibial_pulses_desc  = models.CharField(max_length = 200, blank = True)
    l_posterior_tibial_pulses_desc  = models.CharField(max_length = 200, blank = True)

class Phys_Exam(models.Model):
    patient                         = models.ForeignKey(Patient, on_delete = models.CASCADE)
    date_time                       = models.DateTimeField(null = False, blank = False)
    examining_doctor                = models.CharField(max_length = 75, blank = False, null = False)
    weight_lbs                      = models.DecimalField(max_digits = 7, decimal_places = 3)
    physique                        = models.CharField(max_length = 200, blank = True)
    vitals                          = models.OneToOneField(Phys_Exam_Vitals, on_delete = models.PROTECT)
    lymph_nodes_desc                = models.TextField(blank = True)
    chest_desc                      = models.TextField(blank = True)
    heart                           = models.OneToOneField(Phys_Exam_Heart, on_delete = models.PROTECT)
    abdomen_desc                    = models.TextField(blank = True)
    extremities_desc                = models.TextField(blank = True)
    neurological_desc               = models.TextField(blank = True)
    pelvic_desc                     = models.TextField(blank = True)
    genitalia_desc                  = models.TextField(blank = True)
    rectal_desc                     = models.TextField(blank = True)
    formulation                     = models.TextField(blank = True)
    impression                      = models.TextField(blank = True)
    plan                            = models.TextField(blank = True)

