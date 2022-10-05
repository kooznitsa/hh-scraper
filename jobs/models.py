from django.db import models


class Addresses(models.Model):
    city = models.ForeignKey('Cities', models.DO_NOTHING, blank=True, null=True)
    employer = models.ForeignKey('Employers', models.DO_NOTHING)
    address = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresses'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cities(models.Model):
    city = models.CharField(unique=True, max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cities'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employers(models.Model):
    city = models.ForeignKey(Cities, models.DO_NOTHING, blank=True, null=True)
    employer = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'employers'


class EmploymentModes(models.Model):
    employment_mode = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'employment_modes'


class Experiences(models.Model):
    experience = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'experiences'


class JobEmploymentModes(models.Model):
    job = models.OneToOneField('Jobs', models.DO_NOTHING, primary_key=True)
    employment_mode = models.ForeignKey(EmploymentModes, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'job_employment_modes'
        unique_together = (('job', 'employment_mode'),)


class JobSkills(models.Model):
    job = models.OneToOneField('Jobs', models.DO_NOTHING, primary_key=True)
    skill = models.ForeignKey('Skills', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'job_skills'
        unique_together = (('job', 'skill'),)


class Jobs(models.Model):
    url = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=50)
    salary_from = models.IntegerField(blank=True, null=True)
    salary_to = models.IntegerField(blank=True, null=True)
    salary_mode = models.ForeignKey('SalaryModes', models.DO_NOTHING, blank=True, null=True)
    address = models.ForeignKey(Addresses, models.DO_NOTHING, blank=True, null=True)
    experience = models.ForeignKey(Experiences, models.DO_NOTHING, blank=True, null=True)
    date = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    employer = models.ForeignKey(Employers, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jobs'


class SalaryModes(models.Model):
    salary_mode = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'salary_modes'


class Skills(models.Model):
    skill = models.CharField(unique=True, max_length=300)

    class Meta:
        managed = False
        db_table = 'skills'
