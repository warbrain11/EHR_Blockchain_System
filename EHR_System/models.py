from django.db import models
from datetime import datetime
from django.utils import timezone
from rest_framework.authtoken.models import Token
from EHR_System.managers import *
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from blockchain.models import *
from blockchain_server import settings
from blockchain.models import update_hash, User
import json

#from django.http import JsonResponse

class Patient(models.Model):
    first_name                      = models.CharField(max_length = 36, blank = False, null = False)
    last_name                       = models.CharField(max_length = 36, blank = False, null = False)
    primary_phone                   = models.CharField(max_length = 13, blank = False, null = False)
    cell_phone                      = models.CharField(max_length = 13, blank = False, null = False)
    email                           = models.EmailField(blank = False, null = False)
    Users                           = models.ManyToManyField(User, related_name = "Users")

class Emergency_Contacts(models.Model):
    patient                         = models.ForeignKey(Patient, on_delete = models.CASCADE)
    first_name                      = models.CharField(max_length = 36, blank = False, null = False)
    last_name                       = models.CharField(max_length = 36, blank = False, null = False)
    primary_phone                   = models.CharField(max_length = 13, blank = False, null = False)
    email                           = models.EmailField(blank = True, null = False)
    relationship_to_patient         = models.CharField(max_length = 26, blank = False, null = False)
    
class Patient_Demographics(models.Model):
    patient                         = models.OneToOneField(Patient, on_delete = models.CASCADE, primary_key = True, related_name = 'patient_demographics')
    ethnicity                       = models.CharField(max_length = 36, blank = True, null = False)
    race                            = models.CharField(max_length = 36, blank = True, null = False)
    gender                          = models.CharField(max_length = 36, blank = True, null = False)
    sex                             = models.CharField(max_length = 36, blank = False, null = False)
    date_of_birth                   = models.DateTimeField(blank = False, null = False, default = timezone.now)
    age                             = models.IntegerField(null = False, default = 0)
    height                          = models.DecimalField(max_digits = 6, decimal_places = 3, null = True)                  #Default in inches
    weight                          = models.DecimalField(max_digits = 6, decimal_places = 3, null = True)                  #Default in pounds
    body_mass_index                 = models.DecimalField(max_digits = 6, decimal_places = 3)
    primary_language                = models.CharField(max_length = 36, blank = True)
    hair_color                      = models.CharField(max_length = 36, blank = True)
    eye_color                       = models.CharField(max_length = 36, blank = True)
    dominant_hand                   = models.CharField(max_length = 36, blank = True)

    objects                         = Patient_Demographics_Manager()
    
    class Meta:
        db_table = 'Patient_Demographics'


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
    reason                          = models.CharField(max_length = 150, null = False, blank = True)
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
    height_in                       = models.DecimalField(max_digits = 6, decimal_places = 3, null = True)                  #Default in inches
    weight_lbs                      = models.DecimalField(max_digits = 6, decimal_places = 3, null = True)                  #Default in pounds                        = models.CharField(max_length = 200, blank = True)
    vitals                          = models.OneToOneField(Phys_Exam_Vitals, on_delete = models.PROTECT, null = True, related_name = 'phys_exam')
    lymph_nodes_desc                = models.TextField(blank = True, default = '')
    chest_desc                      = models.TextField(blank = True, default = '')
    heart                           = models.OneToOneField(Phys_Exam_Heart, on_delete = models.PROTECT, null = True, related_name = 'phys_exam')
    abdomen_desc                    = models.TextField(blank = True, default = '')
    extremities_desc                = models.TextField(blank = True, default = '')
    neurological_desc               = models.TextField(blank = True, default = '')
    pelvic_desc                     = models.TextField(blank = True, default = '')
    genitalia_desc                  = models.TextField(blank = True, default = '')
    rectal_desc                     = models.TextField(blank = True, default = '')
    formulation                     = models.TextField(blank = True, default = '')
    impression                      = models.TextField(blank = True, default = '')
    plan                            = models.TextField(blank = True, default = '')


    class Meta:
        db_table = 'Phys_Exam'

"""
@receiver(post_save, sender = Phys_Exam)
def update_demographics(sender, instance, **kwargs):
    height = instance.height_in
    weight = instance.weight_lbs
    patient = instance.patient
    pd = Patient_Demographics.objects.get(patient = patient)
    update_these = []

    if(weight):
        update_these.append['weight']

    if(height):
        update_these.append['height']

    if(update_these != []):
        pd.save(update_fields = update_these)
"""


@receiver(post_save, sender = Patient)
def save_patient_post(sender, instance, **kwargs):  
    signals.pre_save.disconnect(update_hash, sender = blockchain)  

    block_data = {}
    block_data['db_op'] = 'Save'
    block_data['table'] = instance._meta.db_table  
    block_data['first_name'] = instance.first_name
    block_data['last_name'] = instance.last_name
    block_data['primary_phone'] = instance.primary_phone
    block_data['email'] = instance.email

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = Emergency_Contacts)
def save_emergency_contact_post(sender, instance, **kwargs):  
    signals.pre_save.disconnect(update_hash, sender = blockchain)  

    block_data = {}
    block_data['db_op'] = 'Save'
    block_data['table'] = instance._meta.db_table    
    block_data['patient'] = instance.patient
    block_data['first_name'] = instance.first_name
    block_data['last_name'] = instance.last_name
    block_data['primary_phone'] = instance.primary_phone
    block_data['email'] = instance.email
    block_data['relationship_to_patient'] = instance.relationship_to_patient

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = Patient_Demographics)
def save_patient_demographics_post(sender, instance, **kwargs): 
    signals.pre_save.disconnect(update_hash, sender = blockchain)  
 
    block_data = {}
    block_data['db_op'] = 'Save'
    block_data['table'] = instance._meta.db_table    
    block_data['patient'] = instance.patient.id
    block_data['ethnicity'] = instance.ethnicity
    block_data['race'] = instance.race
    block_data['gender'] = instance.gender
    block_data['sex'] = instance.sex
    block_data['date_of_birth'] = instance.date_of_birth
    block_data['age'] = instance.age
    block_data['height'] = float(instance.height)
    block_data['weight'] = float(instance.weight)
    block_data['body_mass_index'] = float(instance.body_mass_index)
    block_data['primary_language'] = instance.primary_language
    block_data['hair_color'] = instance.hair_color
    block_data['eye_color'] = instance.eye_color
    block_data['dominant_hand'] = instance.dominant_hand

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = Medication)
def save_medication_post(sender, instance, **kwargs): 
    signals.pre_save.disconnect(update_hash, sender = blockchain)  
 
    block_data = {}
    block_data['db_op'] = 'Save'
    block_data['table'] = instance._meta.db_table    
    block_data['patient'] = instance.patient.id
    block_data['medication'] = instance.medication
    block_data['frequency_description'] = instance.frequency_description

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = Allergies)
def save_allergies_post(sender, instance, **kwargs):  
    signals.pre_save.disconnect(update_hash, sender = blockchain)  

    block_data = {}
    block_data['db_op'] = 'Save'
    block_data['table'] = instance._meta.db_table    
    block_data['patient'] = instance.patient.id
    block_data['allergic_to'] = instance.allergic_to
    block_data['allergy_notes'] = instance.allergy_notes

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = Immunizations)
def save_immunization_post(sender, instance, **kwargs):  
    signals.pre_save.disconnect(update_hash, sender = blockchain)  

    block_data = {}
    block_data['db_op'] = 'Save'
    block_data['table'] = instance._meta.db_table    
    block_data['patient'] = instance.patient.id
    block_data['vaccine'] = instance.vaccine
    block_data['date_time'] = instance.date_time.isoformat()
    block_data['complications'] = instance.complications

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = Medical_Visits)
def save_medical_visit_post(sender, instance, **kwargs):  
    signals.pre_save.disconnect(update_hash, sender = blockchain)  

    block_data = {}
    block_data['db_op'] = 'Save'
    block_data['table'] = instance._meta.db_table    
    block_data['patient'] = instance.patient.id
    block_data['reason'] = instance.reason
    block_data['main_complaint'] = instance.main_complaint
    block_data['description'] = instance.description
    block_data['type_of_visit'] = instance.type_of_visit
    block_data['examining_doctor'] = instance.examining_doctor

    if(instance.date_time is not None):
        block_data['date_time'] = instance.date_time.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        block_data['date_time'] = ''

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = Surgical_History)
def save_surgical_history_post(sender, instance, **kwargs):  
    signals.pre_save.disconnect(update_hash, sender = blockchain)  

    block_data = {}
    block_data['db_op'] = 'Save' 
    block_data['table'] = instance._meta.db_table   
    block_data['patient'] = instance.patient.id
    block_data['date_time'] = instance.date_time.strftime("%Y-%m-%dT%H:%M:%S")
    block_data['duration'] = instance.duration.strftime("%H:%M:%S")
    block_data['operating_doctors'] = instance.operating_doctors
    block_data['notes'] = instance.notes
    block_data['outcome'] = instance.outcome
    block_data['complications'] = instance.complications

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = History_Of_Transfusions)
def save_transfusion_history_post(sender, instance, **kwargs):
    signals.pre_save.disconnect(update_hash, sender = blockchain)  
  
    block_data = {}
    block_data['db_op'] = 'Save'  
    block_data['table'] = instance._meta.db_table  
    block_data['patient'] = instance.patient.id
    block_data['reason'] = instance.reason
    block_data['units'] = float(instance.units)
    block_data['type_of_transfusion'] = instance.type_of_transfusion
    block_data['veinous_access_device'] = instance.veinous_access_device
    block_data['infusion_device'] = instance.infusion_device
    block_data['infusion_device_settings'] = instance.infusion_device_settings
    block_data['blood_type'] = instance.blood_type
    block_data['complications'] = instance.complications
    block_data['notes'] = instance.notes

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = History_Of_Present_Illness)
def save_history_of_present_illness_post(sender, instance, **kwargs): 
    signals.pre_save.disconnect(update_hash, sender = blockchain)  
 
    block_data = {}
    block_data['db_op'] = 'Save'  
    block_data['table'] = instance._meta.db_table  
    block_data['patient'] = instance.patient.id
    block_data['onset'] = instance.onset.strftime("%Y-%m-%dT%H:%M:%S")
    block_data['illness'] = instance.illness
    block_data['body_location'] = instance.body_location
    block_data['description'] = instance.description
    block_data['aggravating_factors'] = instance.aggravating_factors
    block_data['alleviating_factors'] = instance.alleviating_factors

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = Family_History)
def save_family_history_illness_post(sender, instance, **kwargs):
    signals.pre_save.disconnect(update_hash, sender = blockchain)  
  
    block_data = {}
    block_data['db_op'] = 'Save'  
    block_data['table'] = instance._meta.db_table  
    block_data['patient'] = instance.patient.id
    block_data['family_first_name'] = instance.family_first_name
    block_data['family_last_name'] = instance.family_last_name
    block_data['relationship_to_patient'] = instance.relationship_to_patient
    block_data['health_status'] = instance.health_status

    if(instance.date_of_birth is not None):
        block_data['date_of_birth'] = instance.date_cured.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        block_data['date_of_birth'] = ''

    if(instance.date_of_death is not None):
        block_data['date_of_death'] = instance.date_cured.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        block_data['date_of_death'] = ''

    block_data['cause_of_death'] = instance.cause_of_death
    block_data['description_of_illnesses'] = instance.description_of_illnesses

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = History_Of_Illnesses)
def save_illness_history_post(sender, instance, **kwargs):  
    signals.pre_save.disconnect(update_hash, sender = blockchain)  

    block_data = {}
    block_data['db_op'] = 'Save' 
    block_data['table'] = instance._meta.db_table   
    block_data['patient'] = instance.patient.id
    block_data['onset_date'] = instance.onset_date.strftime("%Y-%m-%dT%H:%M:%S")

    if(instance.date_cured is not None):
        block_data['date_cured'] = instance.date_cured.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        block_data['date_cured'] = ''

    block_data['illness'] = instance.illness
    block_data['body_location'] = instance.body_location
    block_data['description'] = instance.description
    block_data['aggravating_factors'] = instance.aggravating_factors
    block_data['alleviating_factors'] = instance.alleviating_factors

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = Disabilities)
def save_disabilities_post(sender, instance, **kwargs):
    signals.pre_save.disconnect(update_hash, sender = blockchain)  
  
    block_data = {}
    block_data['db_op'] = 'Save'  
    block_data['table'] = instance._meta.db_table  
    block_data['patient'] = instance.patient.id
    block_data['onset_date'] = instance.onset_date.strftime("%Y-%m-%dT%H:%M:%S")
    block_data['disability'] = instance.disability
    block_data['description'] = instance.description
    block_data['aggravating_factors'] = instance.aggravating_factors
    block_data['alleviating_factors'] = instance.alleviating_factors

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = Phys_Exam_Vitals)
def save_exam_vitals_post(sender, instance, **kwargs):  
    signals.pre_save.disconnect(update_hash, sender = blockchain)  

    block_data = {}
    block_data['db_op'] = 'Save'  
    block_data['table'] = instance._meta.db_table
    block_data['pressure_right_palpatation'] = instance.pressure_right_palpatation
    block_data['pressure_left_palpatation'] = instance.pressure_left_palpatation
    block_data['pressure_right_auscultation'] = instance.pressure_right_auscultation
    block_data['pressure_left_auscultation'] = instance.pressure_left_auscultation
    block_data['heart_rate'] = instance.heart_rate
    block_data['respiration_rate'] = instance.respiration_rate
    block_data['temperature_celcius'] = float(instance.temperature_celcius)

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = Phys_Exam_Heart)
def save_exam_heart_post(sender, instance, **kwargs):
    signals.pre_save.disconnect(update_hash, sender = blockchain)  

    block_data = {}
    block_data['db_op'] = 'Save'  
    block_data['table'] = instance._meta.db_table
    block_data['description'] = instance.description
    block_data['r_carotid_pulses_desc'] = instance.r_carotid_pulses_desc
    block_data['l_carotid_pulses_desc'] = instance.l_carotid_pulses_desc
    block_data['r_brachial_pulses_desc'] = instance.r_brachial_pulses_desc
    block_data['l_brachial_pulses_desc'] = instance.l_brachial_pulses_desc
    block_data['r_radial_pulses_desc'] = instance.r_radial_pulses_desc
    block_data['l_radial_pulses_desc'] = instance.l_radial_pulses_desc
    block_data['r_femoral_pulses_desc'] = instance.r_femoral_pulses_desc
    block_data['l_femoral_pulses_desc'] = instance.l_femoral_pulses_desc
    block_data['r_dorsalis_pedis_pulses_desc'] = instance.r_dorsalis_pedis_pulses_desc
    block_data['l_dorsalis_pedis_pulses_desc'] = instance.l_dorsalis_pedis_pulses_desc
    block_data['r_posterior_tibial_pulses_desc'] = instance.r_posterior_tibial_pulses_desc
    block_data['l_posterior_tibial_pulses_desc'] = instance.l_posterior_tibial_pulses_desc

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)

    signals.pre_save.connect(update_hash, sender = blockchain)

@receiver(post_save, sender = Phys_Exam)
def save_exam_post(sender, instance, **kwargs):  
    signals.pre_save.disconnect(update_hash, sender = blockchain)  

    block_data = {}
    block_data['db_op'] = 'Save'  
    block_data['table'] = instance._meta.db_table  
    block_data['patient'] = instance.patient.id
    block_data['date_time'] = instance.date_time.strftime("%Y-%m-%dT%H:%M:%S")
    block_data['examining_doctor'] = instance.examining_doctor
    block_data['height_in'] = float(instance.height_in)
    block_data['weight_lbs'] = float(instance.weight_lbs)
    block_data['vitals'] = instance.vitals.id
    block_data['lymph_nodes_desc'] = instance.lymph_nodes_desc
    block_data['chest_desc'] = instance.chest_desc
    block_data['heart'] = instance.heart.id
    block_data['abdomen_desc'] = instance.abdomen_desc
    block_data['extremities_desc'] = instance.extremities_desc
    block_data['neurological_desc'] = instance.neurological_desc
    block_data['pelvic_desc'] = instance.pelvic_desc
    block_data['genitalia_desc'] = instance.genitalia_desc
    block_data['rectal_desc'] = instance.rectal_desc
    block_data['formulation'] = instance.formulation
    block_data['impression'] = instance.impression
    block_data['plan'] = instance.plan

    block_data = json.dumps(block_data)

    #Creates Genesis Block in the blockchain if one hasn't been created already
    blockchain.objects.add_block(block_data)
    signals.pre_save.connect(update_hash, sender = blockchain)








