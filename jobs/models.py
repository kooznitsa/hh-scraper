from django.db import models


class Cities(models.Model):
    city = models.CharField(unique=True, max_length=50, blank=True, null=True)

    def __str__(self):
        return self.city

    class Meta:
        managed = False
        db_table = 'cities'


class Employers(models.Model):
    city = models.ForeignKey(Cities, models.DO_NOTHING, blank=True, null=True)
    employer = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.employer

    class Meta:
        managed = False
        db_table = 'employers'


class Addresses(models.Model):
    city = models.ForeignKey(Cities, models.DO_NOTHING, blank=True, null=True)
    employer = models.ForeignKey(Employers, models.DO_NOTHING)
    address = models.CharField(unique=True, max_length=255, blank=True, null=True)

    def __str__(self):
        return self.address

    class Meta:
        managed = False
        db_table = 'addresses'


class EmploymentModes(models.Model):
    employment_mode = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.employment_mode

    class Meta:
        managed = False
        db_table = 'employment_modes'


class Experiences(models.Model):
    experience = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.experience

    class Meta:
        managed = False
        db_table = 'experiences'


class SalaryModes(models.Model):
    salary_mode = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.salary_mode

    class Meta:
        managed = False
        db_table = 'salary_modes'


class Jobs(models.Model):
    url = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=50)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_mode = models.ForeignKey(SalaryModes, models.DO_NOTHING, blank=True, null=True)
    address = models.ForeignKey(Addresses, models.DO_NOTHING, blank=True, null=True)
    experience = models.ForeignKey(Experiences, models.DO_NOTHING, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    employer = models.ForeignKey(Employers, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'jobs'
        ordering = ['-date']


class Skills(models.Model):
    skill = models.CharField(unique=True, max_length=300)

    def __str__(self):
        return self.skill

    class Meta:
        managed = False
        db_table = 'skills'


class JobSkills(models.Model):
    job = models.OneToOneField(Jobs, models.DO_NOTHING, primary_key=True)
    skill = models.ForeignKey(Skills, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'job_skills'
        unique_together = (('job', 'skill'),)


class JobEmploymentModes(models.Model):
    job = models.OneToOneField(Jobs, models.DO_NOTHING, primary_key=True)
    employment_mode = models.ForeignKey(EmploymentModes, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'job_employment_modes'
        unique_together = (('job', 'employment_mode'),)