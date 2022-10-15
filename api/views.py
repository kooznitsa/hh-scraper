from django.shortcuts import render
from rest_framework import generics
from jobs.models import Jobs
from .serializers import JobsSerializer


class JobListView(generics.ListAPIView):
    queryset = Jobs.objects.all()
    serializer_class = JobsSerializer