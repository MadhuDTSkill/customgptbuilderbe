from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

class UserIDJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        # Validate the token
        validated_token = self.get_validated_token(raw_token)

        # Get the user_id from the token payload
        user_id = validated_token.get('user_id')
        if not user_id:
            raise exceptions.AuthenticationFailed('User ID not found in token')

        # Instead of returning a full user object, return just the user_id
        return (user_id, validated_token)
