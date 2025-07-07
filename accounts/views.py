from django.shortcuts import render
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.request import  Request
from rest_framework.response import Response 
from . import models
from . import serializers 
from django.contrib.auth import get_user_model,update_session_auth_hash

# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework import status
@api_view(['GET'])
def get_governments(request: Request):
    govs = models.Government.objects.all()
    serializer = serializers.GovermentSerializer(govs, many=True)
    return Response(data={"data":serializer.data}, status=status.HTTP_200_OK)
@api_view(['GET'])
def get_regions(request: Request, pk:int):
    try:
        regions = models.Region.objects.all().filter(government_id=pk)
        serializer = serializers.RegionSerialzer(regions, many=True)
        return Response(data={"data":serializer.data}, status=status.HTTP_200_OK)
    except models.Region.DoesNotExist:
        return Response(data={"error": "Regions not found for the given government"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request: Request):
    try:
        profile = models.Profile.objects.get(user=request.user)
        serializer = serializers.ProfileSerializer(profile)
        return Response(data={"data":serializer.data}, status=status.HTTP_200_OK)
    except models.Profile.DoesNotExist:
        return Response(data={"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
def update_profile(request: Request):
    try:
        user = request.user
        profile = models.Profile.objects.get(user=user)
        serializer = serializers.ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"data":serializer.data}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except models.Profile.DoesNotExist:
        return Response(data={"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_user(request: Request):
    try:
        phone_number = request.data.get("phone_number")
        if models.Profile.objects.filter(phone_number=phone_number).exists():
            return Response(
                data={"error": "user alrady exsists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = serializers.ProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save()

            # استخراج التوكنات للمستخدم الجديد
            # refresh = RefreshToken.for_user(profile.user)

            token , created = Token.objects.get_or_create(user=profile.user)
            tokens = {
                'refresh': str(token.key),
                'access': str(token.key),
            }

            response_data = {
                'profile': serializer.data,
                'tokens': tokens,
            }

            return Response(data=response_data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def sign_in(request: Request):

    username = request.data.get('phone_number')
    password = request.data.get('password')
    if not username or not password:
        return Response(data={"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    try :
        profile = models.Profile.objects.get(phone_number=username)
        print("كلمة السر المدخلة:", password)
        print("كلمة السر المخزنة:", profile.user.password)
        print("التحقق:", profile.user.check_password(password))
        if profile.user.check_password(password):
            token ,created = Token.objects.get_or_create(user = profile.user)
            tokens = {
                'refresh': str(token.key),
                'access': str(token.key),
            }
            serializer = serializers.ProfileSerializer(profile)
            return Response(data={"profile": serializer.data, "tokens": tokens}, status=status.HTTP_200_OK)
        else:
            return Response(data={"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response(data={"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["PUT"])
def update_password(request: Request):  # تصحيح إملائي في اسم الدالة (اختياري)
    User = get_user_model()
    # 1. تصحيح الخطأ الإملائي في اسم الحقل
    password = request.data.get("password")  # "password" بدلاً من "passowrd"
    
    # 2. التحقق من وجود كلمة المرور
    if not password:
        return Response(
            data={"error": "Password field is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(pk=request.user.id)
        # 3. استخدام الدالة الصحيحة لتحديث كلمة المرور
        user.set_password(password)
        user.save()
        
        # 4. (اختياري) تسجيل الخروج من جميع الجلسات
        update_session_auth_hash(request, user)  # يتطلب استيراد: from django.contrib.auth import update_session_auth_hash
        
        return Response(data={"Success": "Password updated successfully"}, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
        return Response(data={"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # تسجيل الخطأ للتصحيح
        return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)