from datetime import datetime, timedelta

from django.shortcuts import render
from django.db.models import Q

from .models import Jobs, JobSkills, JobEmploymentModes


def jobs(request):
    jobs = Jobs.objects.filter(
        date__gte=datetime.now()-timedelta(days=1), address__city=1
    ).order_by('id')
    context = {'jobs': jobs}
    return render(request, 'jobs/jobs.html', context)


def job(request, pk):
    job = Jobs.objects.get(id=pk)
    skills = JobSkills.objects.filter(Q(job=job.id))
    modes = JobEmploymentModes.objects.filter(Q(job=job.id))
    context = {'job': job, 'skills': skills, 'modes': modes}
    return render(request, 'jobs/job.html', context)