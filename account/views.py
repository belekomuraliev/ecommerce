from django.shortcuts import render
from rest_framework import generics, status
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import ProfileSerializer
from .models import Profile, User


class ProfileRegisterView(viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


    def create_profile(self, request, is_sender):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save(is_sender=is_sender)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def sender(self, request, pk=None):
        return self.create_profile(request, True)

    @action(methods=['POST'], detail=False)
    def bayer(self, request, pk=None):
        return self.create_profile(request, False)