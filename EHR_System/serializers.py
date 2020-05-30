from rest_framework import serializers
from EHR_System.models import *
from datetime import datetime

class Patient_Demographics_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Patient_Demographics
        fields = '__all__'

class Emergency_Contacts_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Emergency_Contacts
        fields = '__all__'

class Patient_Serializer(serializers.ModelSerializer):
    patient_demographics = Patient_Demographics()
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'primary_phone', 'cell_phone', 'email']

    def save(self):
        patient = Patient(
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            primary_phone = self.validated_data['primary_phone'],
            cell_phone = self.validated_data['cell_phone'],
            email = (self.validated_data['email']).lower(),
        )

        patient.save()

        return patient

class Medication_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'

class Allergies_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Allergies
        fields = '__all__'

class Immunizations_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Immunizations
        fields = '__all__'

class Medical_Visits_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Medical_Visits
        fields = '__all__'

class Surgical_History_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Surgical_History
        fields = '__all__'

class History_Of_Transfusions_Serializer(serializers.ModelSerializer):
    class Meta:
        model = History_Of_Transfusions
        fields = '__all__'

class History_Of_Present_Illness_Serializer(serializers.ModelSerializer):
    class Meta:
        model = History_Of_Present_Illness
        fields = '__all__'

class Family_History_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Family_History
        fields = '__all__'

class History_Of_Illnesses_Serializer(serializers.ModelSerializer):
    class Meta:
        model = History_Of_Illnesses
        fields = '__all__'

class Disabilities_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Disabilities
        fields = '__all__'

class Phys_Exam_Vitals_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Phys_Exam_Vitals
        fields = '__all__'

class Phys_Exam_Heart_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Phys_Exam_Heart
        fields = '__all__'

class Phys_Exam_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Phys_Exam
        fields = '__all__'

    def save(self):
        phys_exam = Phys_Exam(
            patient = self.validated_data['patient'],
            date_time = self.validated_data['date_time'],
            examining_doctor = self.validated_data['examining_doctor'],
            height_in = self.validated_data['height_in'],
            weight_lbs = self.validated_data['weight_lbs'],
            vitals = self.validated_data['vitals'],
            lymph_nodes_desc = self.validated_data['lymph_nodes_desc'],
            chest_desc = self.validated_data['chest_desc'],
            heart = self.validated_data['heart'],
            abdomen_desc = self.validated_data['abdomen_desc'],
            extremities_desc = self.validated_data['extremities_desc'],
            neurological_desc = self.validated_data['neurological_desc'],
            pelvic_desc = self.validated_data['pelvic_desc'],
            genitalia_desc = self.validated_data['genitalia_desc'],
            rectal_desc = self.validated_data['rectal_desc'],
            formulation = self.validated_data['formulation'],
            impression = self.validated_data['impression'],
            plan = self.validated_data['plan']
        )
        
        #p = Patient.objects.get(id = self.validated_data['patient'])
        pd = Patient_Demographics.objects.get(patient = self.validated_data['patient'])

        height = self.validated_data['height_in']
        weight = self.validated_data['weight_lbs']

        if(height):
            pd.height = height
            pd.save(update_fields = ['height'])
        
        if(weight):
            pd.weight = weight
            pd.save(update_fields = ['weight'])

        phys_exam.save()

        return phys_exam



    





