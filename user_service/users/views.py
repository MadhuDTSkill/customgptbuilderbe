from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserLogoutSerializer
from .permissions import IsUserIDAuthenticated

User = get_user_model()

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        print(request.headers['Content-Length'])
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        return Response({'detail': 'Invalid credentials'}, status=400)

class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsUserIDAuthenticated]
    serializer_class = UserLogoutSerializer

    def post(self, request):
        refresh_token = request.data.get("refresh")
        
        if not refresh_token:
            return Response({'detail': 'Refresh token is required'}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logged out'}, status=205)
        
        except TokenError:
            return Response({'detail': 'Invalid refresh token'}, status=400)
        except Exception:
            return Response({'detail': 'Error occurred while logging out'}, status=500)

class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [IsUserIDAuthenticated]
    
    def get(self, request):
        user = self.queryset.get(id=request.user)
        user_data = self.serializer_class(user).data
        return Response(user_data)
    