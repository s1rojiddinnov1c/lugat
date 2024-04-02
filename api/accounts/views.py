from django.shortcuts import render,get_object_or_404
from rest_framework.generics import CreateAPIView, GenericAPIView,UpdateAPIView,ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializer import (SignUpSerializer, 
                         LoginSerializer, 
                         UpdateSerializer, 
                         LogoutSerializer, 
                         ChangePasswordSerializer,
                         UserProfileSerializer,
                         PasswordResetSerializer,
                         PasswordResetViaCodeSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash 
from rest_framework.views import APIView
from .utils import send_email
import datetime
from django.contrib.auth import get_user_model
from rest_framework import permissions
from django.http import JsonResponse
import jwt


class SignUpApiView(CreateAPIView):
    permission_classes = (AllowAny, )
    queryset = get_user_model()
    serializer_class = SignUpSerializer


class LoginApiView(TokenObtainPairView):
    serializer_class = LoginSerializer


class UpdateTokenApiView(TokenRefreshView):
    serializer_class = UpdateSerializer


class LogoutApiView(GenericAPIView):
    
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated, ]
    
    def post(self, request):
        
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        data = {
            "message" : "siz tizimdan chiqdingiz"
        }
        
        return Response(data, status = status.HTTP_204_NO_CONTENT)


class ChangePasswordView(UpdateAPIView):
        
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_passvord foydalanuvchi oladigan parolni ham xesh qiladi
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()

                response = {
                    'message': 'Parolingiz ozgartirildi!',
                    
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(APIView):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request):
        user = self.queryset.get(id=request.user.id)
        sz = self.serializer_class(user).data
        return Response(data={"status":True, 'data':sz})






class PasswordResetView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = PasswordResetSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = get_object_or_404(User, email=email)
        code = user.create_verify_code()

        data = {
            'status' : True,
            'message' : 'you get email via verify code'
        }
        send_email(email, code)
        return Response(data)


class PasswordResetViaCodeView(APIView):
    serializer_class = PasswordResetViaCodeSerializer
    permission_classes = (AllowAny, )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        password = serializer.validated_data.get('password1')
        verify_code = User.objects.filter(code_lifetime__gte = datetime.now(), code = code, is_confirmed=False)
        if verify_code.exists():
            user = verify_code.first().user
            user.set_password(password)
            user.save()
            verify_code.update(is_confirmed = True)
            data = {
                'status' : True,
                'message' : 'password reseted👍'
            }
            return Response(data)
        data = {
            'status' : False,
            'message' : 'we can not find this verification code'
        }
        return Response(data)




    

  

