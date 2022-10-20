from datetime import datetime, timedelta

from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from jobs.models import Jobs, JobEmploymentModes, JobSkills
from .serializers import JobsSerializer, JobEmploymentModesSerializer, JobSkillsSerializer


class JobListView(ListAPIView):
    serializer_class_JobsSerializer = JobsSerializer
    serializer_class_JobEmploymentModes = JobEmploymentModesSerializer
    serializer_class_JobSkills = JobSkillsSerializer

    def get_queryset_Jobs(self):
        return Jobs.objects.filter(
            date__gte=datetime.now()-timedelta(days=1), address__city=1).order_by('id')

    def get_queryset_JobEmploymentModes(self):
        return JobEmploymentModes.objects.distinct('job_id').all()

    def get_queryset_JobSkills(self):
        return JobSkills.objects.distinct('job_id').all()

    def concat_dict(self, d):
        for i in range(len(d['JOBS'])):
            for j in range(len(d['EMP_MODES'])):
                if d['JOBS'][i]['id'] == d['EMP_MODES'][j]['job_id']:
                    d['JOBS'][i]['employment_modes'] = d['EMP_MODES'][j]['employment_mode_id']

            for k in range(len(d['SKILLS'])):
                if d['JOBS'][i]['id'] == d['SKILLS'][k]['job_id']:
                    d['JOBS'][i]['skills'] = d['SKILLS'][k]['skill_id']
        return d

    def list(self, request, *args, **kwargs):
        jobs = self.serializer_class_JobsSerializer(self.get_queryset_Jobs(), many=True)
        job_employment_modes = self.serializer_class_JobEmploymentModes(self.get_queryset_JobEmploymentModes(), many=True)
        job_skills = self.serializer_class_JobSkills(self.get_queryset_JobSkills(), many=True)
        
        d = self.concat_dict({
            'JOBS': jobs.data,
            'EMP_MODES': job_employment_modes.data,
            'SKILLS': job_skills.data,
        })

        del d['EMP_MODES']
        del d['SKILLS']

        return Response(d)