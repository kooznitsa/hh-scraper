from rest_framework import serializers
from jobs.models import Jobs, Addresses, JobEmploymentModes, JobSkills


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
        fields = ('address', 'city',)


class JobSkillsSerializer(serializers.ModelSerializer):
    employment_mode = serializers.SlugRelatedField(
        many=True, 
        read_only=True, 
        slug_field='skill'
    )

    class Meta:
        model = JobSkills
        fields = ('skill',)


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


class JobEmploymentModesSerializer(serializers.ModelSerializer):
    job = JobsSerializer()
    employment_mode = serializers.SlugRelatedField( 
        read_only=True, 
        slug_field='employment_mode'
    )

    class Meta:
        model = JobEmploymentModes
        fields = ('job', 'employment_mode')