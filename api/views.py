from django.shortcuts import render
from rest_framework import generics
from jobs.models import JobEmploymentModes
from .serializers import JobEmploymentModesSerializer


class JobListView(generics.ListAPIView):
    queryset = JobEmploymentModes.objects.all()
    serializer_class = JobEmploymentModesSerializer