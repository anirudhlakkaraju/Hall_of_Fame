from django.contrib.auth.models import User

from rest_framework import serializers

from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)

from userprofile import models

_NAME = 'name'


class ProjectSerializer(TaggitSerializer, serializers.ModelSerializer):
    # Tags get serialized and passed as a list
    tags = TagListSerializerField()
    
    class Meta:
        model = models.Project
        excluded_fields = ("uuid",)
        additional_fields = ("tags",)

        # Method returns tuple of model fields and extra included/excluded fields
        def assign_fields(excluded_fields, *extra_fields):
            return tuple([*[f.name for f in models.Project._meta.fields if f.name not in excluded_fields], *extra_fields])
        fields = assign_fields(excluded_fields, *additional_fields)

    
class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Skill
        excluded_fields = ("profile",)

        # Method returns tuple of model fields and extra excluded fields
        def assign_fields(excluded_fields, *extra_fields):
            return tuple([*[f.name for f in models.Skill._meta.fields if f.name not in excluded_fields], *extra_fields])
        fields = assign_fields(excluded_fields)


class InterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Interest
        excluded_fields = ("profile",)

        # Method returns tuple of model fields and extra excluded fields
        def assign_fields(excluded_fields, *extra_fields):
            return tuple([*[f.name for f in models.Interest._meta.fields if f.name not in excluded_fields], *extra_fields])
        fields = assign_fields(excluded_fields)


class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Experience
        excluded_fields = ("profile",)

        # Method returns tuple of model fields and extra excluded fields
        def assign_fields(excluded_fields, *extra_fields):
            return tuple([*[f.name for f in models.Experience._meta.fields if f.name not in excluded_fields], *extra_fields])
        fields = assign_fields(excluded_fields)


class ProfileDetailSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(read_only=True, many=True)
    skills = SkillSerializer(read_only=True, many=True)
    interests = InterestSerializer(read_only=True, many=True)
    experience = ExperienceSerializer(read_only=True, many=True)
    
    class Meta:
        model = models.Profile
        additional_fields = ("projects", "skills", "interests","experience", )
        excluded_fields = ("uuid", )

        # Method returns tuple of model fields and extra included/excluded fields
        def assign_fields(excluded_fields, *extra_fields):
            return tuple([*[f.name for f in models.Profile._meta.fields if f.name not in excluded_fields], *extra_fields])
        fields = assign_fields(excluded_fields, *additional_fields)
    

class ProfileUpdateSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, required=False)
    interests = InterestSerializer(many=True, required=False)
    experience = ExperienceSerializer(many=True, required=False)
    
    class Meta:
        model = models.Profile
        additional_fields = ("skills", "interests","experience", )
        excluded_fields = ("uuid", )

        # Method returns tuple of model fields and extra included/excluded fields
        def assign_fields(excluded_fields, *extra_fields):
            return tuple([*[f.name for f in models.Profile._meta.fields if f.name not in excluded_fields], *extra_fields])
        fields = assign_fields(excluded_fields, *additional_fields)
    
    def update(self, instance, validated_data):
        if "skills" in validated_data: 
            skills_data = validated_data.pop('skills')
            skills = (instance.skills).all()
            skills = list(skills)

        interests_data = validated_data.pop('interests')
        interests = (instance.interests).all()
        interests = list(interests)

        experience_data = validated_data.pop('experience')
        experience = (instance.experience).all()
        experience = list(experience)
        
        instance.image = validated_data.get('image', instance.image)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.fb_messenger = validated_data.get('fb_messenger', instance.fb_messenger)
        instance.website = validated_data.get('website', instance.website)
        instance.github = validated_data.get('github', instance.github)
        instance.role = validated_data.get('role', instance.role)
        instance.college = validated_data.get('college', instance.college)
        instance.save()

        for skill_data in skills_data:
            skill = skills.pop(1)
            skill.name = skill_data.get('name', skill.name)
            skill.skill_level = skill_data.get('skill_level', skill.skill_level)
            skill.save()

        for interest_data in interests_data:
            interest = interests.pop(0)
            interest.name = interest_data.get('name', interest.name)
            interest.description = interest_data.get('description', interest.description)
            interest.save()

        for exp_data in experience_data:
            exp = experience.pop(0)
            exp.title = exp_data.get('title', exp.title)
            exp.worked_at = exp_data.get('worked_at', exp.worked_at)
            exp.duration = exp_data.get('duration', exp.duration)
            exp.save()
        return instance
