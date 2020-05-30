from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from blockchain.views import *
from EHR_System.get_views import *
from EHR_System.post_views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', Register_User_API),
    path('login/', obtain_auth_token),
    path('api/blockchain/', display_blockchain),
    path('api/patients/', get_patient),
    path('api/patients/create/', add_patient),
    path('api/patients/emergency_contact/', get_emergency_contact),
    path('api/patients/emergency_contact/create/', add_emergency_contact),
    path('api/patients/demographics/', get_patient_demographics),
    path('api/patients/demographics/create/', add_patient_demographics),
    path('api/patients/medications/', get_medication),
    path('api/patients/medications/create/', add_medication),
    path('api/patients/allergies/', get_allergies),
    path('api/patients/allergies/create/', add_allergies),
    path('api/patients/immunizations/', get_immunizations),
    path('api/patients/immunizations/create/', add_immunizations),
    path('api/patients/surgicalHistory/', get_surgical_history),
    path('api/patients/surgicalHistory/create/', add_surgical_history),
    path('api/patients/transfusionHistory/', get_transfusion_history),
    path('api/patients/transfusionHistory/create/', add_transfusion_history),
    path('api/patients/hpi/', get_present_illness_history),
    path('api/patients/hpi/create/', add_present_illness_history),
    path('api/patients/familyHistory/', get_family_history),
    path('api/patients/familyHistory/create/', add_family_history),
    path('api/patients/IllnessHistory/', get_illness_history),
    path('api/patients/IllnessHistory/create/', add_illness_history),
    path('api/patients/Disabilities/', get_disabilities),
    path('api/patients/Disabilities/create/', add_disabilities),
    path('api/patients/examVitals/', get_phys_exam_vitals),
    path('api/patients/examVitals/create/', add_phys_exam_vitals),
    path('api/patients/examHeart/', get_phys_exam_heart),
    path('api/patients/examHeart/create/', add_phys_exam_heart),
    path('api/patients/exam/', get_phys_exam),
    path('api/patients/exam/create/', add_phys_exam),
]
