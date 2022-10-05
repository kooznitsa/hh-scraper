from django.shortcuts import render
from .models import Jobs


def jobs(request):
    jobs = Jobs.objects.all()
    context = {'jobs': jobs}
    return render(request, 'jobs/jobs.html', context)


def job(request, pk):
    job = Jobs.objects.get(id=pk)
    context = {'job': job}
    return render(request, 'jobs/job.html', context)