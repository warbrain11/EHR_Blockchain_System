from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from blockchain.views import *
from EHR_System.get_views import *
from EHR_System.post_views import *
from EHR_System.update_views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('authregister/', Register_Code_Gen),
    path('register/', Register_User_API),
    path('api/users/', Show_Users),
    path('login/', obtain_auth_token),
    path('api/blockchain/', display_blockchain),
    path('api/blockchain/check/', validate_blockchain),
    path('api/blockchain/update/', write_blockchain_file),
    path('api/blockchain/repair/', repair_blockchain),
    path('api/patients/', get_patient),
    path('api/patients/create/', add_patient),
    path('api/patients/update/', update_patient),
    path('api/patients/emergency_contact/', get_emergency_contact),
    path('api/patients/emergency_contact/create/', add_emergency_contact),
    path('api/patients/emergency_contact/update/', update_emergency_contacts),
    path('api/patients/demographics/', get_patient_demographics),
    path('api/patients/demographics/create/', add_patient_demographics),
    path('api/patients/demographics/update/', update_patient_demographics),
    path('api/patients/medications/', get_medication),
    path('api/patients/medications/create/', add_medication),
    path('api/patients/medications/update/', update_medication),
    path('api/patients/allergies/', get_allergies),
    path('api/patients/allergies/create/', add_allergies),
    path('api/patients/allergies/update/', update_allergies),
    path('api/patients/immunizations/', get_immunizations),
    path('api/patients/immunizations/create/', add_immunizations),
    path('api/patients/immunizations/update/', update_immunizations),
    path('api/patients/medical_visits/', get_medical_visits),
    path('api/patients/medical_visits/create/', add_medical_visits),
    path('api/patients/medical_visits/update/', update_medical_visits),
    path('api/patients/surgicalHistory/', get_surgical_history),
    path('api/patients/surgicalHistory/create/', add_surgical_history),
    path('api/patients/surgicalHistory/update/', update_surgical_history),
    path('api/patients/transfusionHistory/', get_transfusion_history),
    path('api/patients/transfusionHistory/create/', add_transfusion_history),
    path('api/patients/transfusionHistory/update/', update_history_of_transfusions),
    path('api/patients/hpi/', get_present_illness_history),
    path('api/patients/hpi/create/', add_present_illness_history),
    path('api/patients/hpi/update/', update_history_of_present_illness),
    path('api/patients/familyHistory/', get_family_history),
    path('api/patients/familyHistory/create/', add_family_history),
    path('api/patients/familyHistory/update/', update_family_history),
    path('api/patients/IllnessHistory/', get_illness_history),
    path('api/patients/IllnessHistory/create/', add_illness_history),
    path('api/patients/IllnessHistory/update/', update_history_of_illnesses),
    path('api/patients/Disabilities/', get_disabilities),
    path('api/patients/Disabilities/create/', add_disabilities),
    path('api/patients/Disabilities/update/', update_disabilities),
    path('api/patients/examVitals/', get_phys_exam_vitals),
    path('api/patients/examVitals/create/', add_phys_exam_vitals),
    path('api/patients/examVitals/update/', update_phys_exam_vitals),
    path('api/patients/examHeart/', get_phys_exam_heart),
    path('api/patients/examHeart/create/', add_phys_exam_heart),
    path('api/patients/examHeart/update/', update_phys_exam_heart),
    path('api/patients/exam/', get_phys_exam),
    path('api/patients/exam/create/', add_phys_exam),
    path('api/patients/exam/update/', update_phys_exam),
]
