from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema


from UserApp.api.serializers import RegistrationSerializers


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)

            # Confirm that the refresh token belongs to the particular user
            if token.get('user_id') != request.user.id:
                return Response(
                    {"detail": "Token does not belong to this user."},
                    status=status.HTTP_403_FORBIDDEN
                )
            token.blacklist()

            return Response(
                {"detail": "Logout successful."},
                status=status.HTTP_205_RESET_CONTENT
            )

        except TokenError:
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST
            )




class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegistrationSerializers,
        responses=RegistrationSerializers,
    )   
    def post(self, request):
        serializers = RegistrationSerializers(data=request.data)

        data = {}

        if serializers.is_valid():
            account = serializers.save()

            data['response'] = "Registration Successful"
            data['username'] = account.username
            data['email'] = account.email

            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializers.errors

            return Response(data, status=status.HTTP_400_BAD_REQUEST)