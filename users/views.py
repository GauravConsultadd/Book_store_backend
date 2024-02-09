from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import authenticate
from django.core.mail import send_mail
import uuid
import os
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes



class RegisterView(APIView):
    serializer_class=RegisterSerializer
    model=CustomUser

    def post(self,request):
        try:
            serializer = self.serializer_class(data=request.data)

            if not serializer.is_valid():
                return Response({'message': serializer.error_messages},status=400)
            
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            role = serializer.validated_data.get('role')
            
            if(role is None or role == 'Buyer'):
                user = self.model.objects.create_buyer(username=username,email=email,password=password)
            elif role == 'Admin':
                user = self.model.objects.create_superuser(username=username,email=email,password=password)
            elif role == 'Seller':
                user = self.model.objects.create_seller(username=username,email=email,password=password)
            else:
                return Response({'message': 'Invalid user role'},status=400)

            print("yaha")
            json_user={
                'username': username,
                'email': email,
                'role': user.role,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            }

            return Response({'user': json_user},status=201)
        except Exception as err:
            return Response({'message':err.args},status=500)
        

class LoginView(APIView):

    serializer_class = LoginSerializer
    model = CustomUser

    def post(self, request):
        try:

            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid(raise_exception=True):
                email = serializer.validated_data["email"]
                password = serializer.validated_data["password"]
                user = authenticate(email=email, password=password)

                if user is not None:
                    
                    if user.is_active:
                        user = self.model.objects.get(email=email)
                        
                        refresh = RefreshToken.for_user(user)
                        access_token = str(refresh.access_token)

                        json_user={
                            'username': user.username,
                            'email': email,
                            'role': user.role,
                            'is_active': user.is_active,
                            'is_staff': user.is_staff,
                            'is_superuser': user.is_superuser,
                        }

                        return Response({
                            "access_token": access_token,
                            "refresh_token": str(refresh),
                            'user': json_user
                            # "refresh_token": refresh
                            },
                            status = 200
                        )
                    else:

                        return Response({
                            "message":"Your account is inactive, please contact our support"
                            },
                            status = 401
                        )
                else:
                    
                    return Response({
                        "message":"Incorrect username or password"
                        },
                        status = 401
                    )
        except Exception as err:
            return Response({'message':err.args},status=500)
        

class Logout(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        try:
            refresh_token = request.data.get('refresh_token')

            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response({
                    'message': 'Logged out successfully'
                },status=205)
            else:
                return Response({
                    'message': 'refresh_token should not be null'
                },status=400)
        except Exception as err:
            return Response({'message':err.args},status=500)
        

class GetCurrentUser(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        user = request.user
        json_user={
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        }
        return Response({'user': json_user},status=200)

class Checker(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        return Response({'message':'Sending response'})
    


class AdminView(APIView):
    permission_classes=[IsAuthenticated,IsAdminUser]
    models = CustomUser

    def get(self,request):
        try:
            users = self.models.objects.all()

            json_users = [{'id': user.id,'username': user.username, 'email': user.email,'is_active': user.is_active,'is_staff': user.is_staff,'is_superuser': user.is_superuser,'role': user.role } for user in users]

            return Response({
                'users': json_users
            },status=200)
        except Exception as err:
            return Response({'message': err.args},status=500)
        
class RoleChange(APIView):
    permission_classes=[IsAuthenticated,IsAdminUser]
    models = CustomUser

    def put(self,request):
        try:
            data = request.data
            role = data.get('role',None)
            id = data.get('id',None)

            if role is None or id is None:
                return Response({'message': 'Invalid request'},status=400) 
            user = self.models.objects.get(id=id)

            user.role = role
            user.save()

            users = self.models.objects.all()
            json_users = [{'id': user.id,'username': user.username, 'email': user.email,'is_active': user.is_active,'is_staff': user.is_staff,'is_superuser': user.is_superuser,'role': user.role } for user in users]

            return Response({
                'users': json_users
            },status=200)

        except Exception as err:
            return Response({'message': err.args},status=500)
        

class ForgotPassword(APIView):
    model = CustomUser
    def post(self,request):
        try:
            email = request.data.get('email',None)
            if email is None:
                return Response({
                    'message': 'Email is required'
                },status=400)
            
            # send_email_to_client(email=email)

            user = self.model.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(str(user.pk).encode())

            reset_link = f'{os.environ.get('BASE_URL')}/reset/{uidb64}/{token}'

            subject="test subject"
            message="test message"
            from_email= os.environ.get('EMAIL_HOST_USER')
            recipients=[email]

            html_message=f'follow the link to reset password {reset_link}'

            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipients,
                html_message=html_message,
                fail_silently=False
            )

            return Response({
                'message' : 'email sent'
            },status=200)
        except Exception as err:
            return Response({'message': err.args},status=500)
        

class ResetPassword(APIView):
    model = CustomUser

    def post(self,request,uidb64,token):
        try:
            data = request.data
            password = data.get('password',None)

            user = check_token(uidb64, token)

            if user:
                user.set_password(password)
                user.save()
                return Response({'detail': 'Password reset successful'}, status=200)

            return Response({'message': 'Invalid user'},status=400)

        except Exception as err:
            return Response({'message': err.args},status=500)
        
    
def check_token(uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            return user
        
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        pass
    return None
    