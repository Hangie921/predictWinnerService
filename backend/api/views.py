from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Weight, Game, Team, TeamStat, Pitcher, PitcherStat
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer,WeightSerializer,GameSerializer
from django.http import JsonResponse, HttpResponse
from . import const 
from operator import itemgetter, attrgetter


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CreateWeightView(generics.ListCreateAPIView):
    queryset = Weight.objects.all()
    serializer_class = WeightSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Weight.objects.filter(owner=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        else:
            print(serializer.errors)

class UpdateWeightView(generics.UpdateAPIView):
    queryset = Weight.objects.all()
    serializer_class = WeightSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Weight.objects.filter(owner=user)

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        else:
            print(serializer.errors)



