from rest_framework import serializers
from .models import Government,Region ,Profile
from django.contrib.auth import get_user_model

User = get_user_model()



class GovermentSerializer(serializers.ModelSerializer):

    class Meta :
        model = Government 
        fields = ['id', 'name']

class RegionSerialzer(serializers.ModelSerializer):
    class Meta :
        model = Region
        fields = ['id', 'name']




User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    goverment_name = serializers.CharField(source='government.name', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)
    
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    phone_number = serializers.CharField()  # سيكون هو الـ username

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'compny_name', 'name', 'email', 'phone_number', 'address',
            'government', 'region', 'goverment_name', 'region_name',
            'created_at', 'updated_at', 'password',"image"
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        password = validated_data.pop('password')
        email = validated_data.pop('email', None)  # اجعله اختياريًا

        # إنشاء المستخدم
        user = User.objects.create_user(
            username=phone_number,
            password=password,
            email=email if email else ''  # إيميل اختياري
        )
       
        # إنشاء البروفايل وربطه بالمستخدم
        profile = Profile.objects.create(
            user=user,
            phone_number=phone_number,
            email=email,
            **validated_data
        )

        return profile