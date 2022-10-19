from rest_framework import serializers

from jobs.models import Jobs, Addresses, JobEmploymentModes, \
        JobSkills, EmploymentModes, Skills


class FlattenMixin(object):
    """Flatens the specified related objects in this representation"""
    def to_representation(self, obj):
        assert hasattr(self.Meta, 'flatten'), (
            'Class {serializer_class} missing "Meta.flatten" attribute'.format(
                serializer_class=self.__class__.__name__
            )
        )
        rep = super(FlattenMixin, self).to_representation(obj)
        for field, serializer_class in self.Meta.flatten:
            serializer = serializer_class(context=self.context)
            objrep = serializer.to_representation(getattr(obj, field))
            for key in objrep:
                rep[key] = objrep[key]
        return rep


class AddressesSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(
        read_only=True, 
        slug_field='city'
    ) 

    class Meta:
        model = Addresses
        fields = ('address', 'city')


class EmploymentModesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentModes
        fields = ('employment_mode',)


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ('skill',)


class JobEmploymentModesSerializer(serializers.ModelSerializer):
    job_id = serializers.SerializerMethodField()
    employment_mode_id = serializers.SerializerMethodField()

    class Meta:
        model = JobEmploymentModes
        fields = ('job_id', 'employment_mode_id')

    def get_job_id(self, obj):
        return obj.job_id

    def get_employment_mode_id(self, obj):
        queryset = obj.__class__.objects.filter(pk=self.get_job_id(obj))
        return [EmploymentModesSerializer(q).data for q in queryset]


class JobSkillsSerializer(serializers.ModelSerializer):
    job_id = serializers.SerializerMethodField()
    skill_id = serializers.SerializerMethodField()

    class Meta:
        model = JobSkills
        fields = ('job_id', 'skill_id')

    def get_job_id(self, obj):
        return obj.job_id

    def get_skill_id(self, obj):
        queryset = obj.__class__.objects.filter(pk=self.get_job_id(obj))
        return [SkillsSerializer(q).data for q in queryset]


class JobsSerializer(FlattenMixin, serializers.ModelSerializer):
    experience = serializers.SlugRelatedField( 
        read_only=True, 
        slug_field='experience'
    )
    employer = serializers.SlugRelatedField( 
        read_only=True, 
        slug_field='employer'
    )

    class Meta:
        model = Jobs
        fields = (
            'id', 'title', 'salary_from', 'salary_to', 
            'experience', 'employer'
        )
        flatten = [('address', AddressesSerializer)]