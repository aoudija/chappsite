from django.shortcuts import render
from .serializers import MatchSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from Models.models import User
# Create your views here.

@permission_classes([AllowAny])
class matchView(APIView):
    print("firstPrint")
    def post(self, request, player, opponent, *args, **kwargs):
        print("secondPrint")
        print(f"***{player} vs {opponent}****")
        p = User.objects.get(username=player)
        o = User.objects.get(username=opponent)
        data = {
            'player': p.id,
            'opponent': o.id
        }
        serializer = MatchSerializer(data=data)
        if serializer.is_valid():
            match = serializer.save()
            match.save()
            return Response({'id': match.id}, status=status.HTTP_201_CREATED)
        return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
