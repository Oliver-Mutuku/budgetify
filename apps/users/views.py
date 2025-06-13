from datetime import datetime, timedelta

import jwt
from django.conf import settings
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User
from .serializers import UserRegistrationSerializer
from apps.utils.token import JWTAuthentication


class UserAuthentication(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def get_authenticators(self):
        if self.request.method == "GET":
            return [JWTAuthentication()]
        return []

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return []

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response({ "data": serializer.data }, status=200)

    def create(self, request):
        data = JSONParser().parse(request)
        username = data["username"]
        password = data["password"]
        remember_me = data["remember_me"]
        try:
            user = get_object_or_404(User, username=username)
        except:
            return Response(status=404)

        if not user.check_password(password):
            return Response(status=400)

        payload = {"id": str(user.id)}

        if not remember_me:
            payload["exp"] = datetime.utcnow() + timedelta(hours=1)

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return Response({"token": token }, status=200)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




