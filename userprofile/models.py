""" Models for User Profile"""
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from taggit.managers import TaggableManager

import uuid

class Profile(models.Model):
    STUDENT = "Student"
    FACULTY = "Faculty"
    ROLE_CHOICES = (
        (STUDENT, "Student"),
        (FACULTY, "Faculty"),
    )
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    phone_number = models.CharField(max_length=14, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    fb_messenger = models.URLField(max_length=256, null=True, blank=True)
    website = models.URLField("Website link", max_length=256, null=True, blank=True)
    github = models.URLField("GitHub link", max_length=256, null=True, blank=True)
    role = models.CharField("Are you student or faculty?", max_length=7, choices=ROLE_CHOICES, default="Student", null=True, blank=False)
    college = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):  
        return str(self.user)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class Project(models.Model):
    ONGOING = "Ongoing"
    COMPLETE = "Complete"
    INACTIVE = "Inactive"
    STATUS_CHOICES = (
        (ONGOING, "Ongoing"),
        (COMPLETE, "Complete"),
        (INACTIVE, "Inactive"),
    )
    # Can make ManytoMany relation if multiple users collaborate. Then on_delete should be protect 
    uuid = models.UUIDField(unique=True, default=uuid.uuid4) 
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.CharField(max_length=256, null=True, blank=False)
    abstract = models.CharField(max_length=500, null=True, blank=False)
    description = models.TextField(null=True, blank=False)
    status = models.CharField("Project status?", max_length=10, choices=STATUS_CHOICES, default="Ongoing", null=True, blank=False)
    tags = TaggableManager()
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):  
        return self.title 

    # Slug field will automatically populate with title on saving a project
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

        
class Skill(models.Model):
    SKILL_LEVEL_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )    
    # user = model.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=128, null=True, blank=False)
    skill_level = models.PositiveSmallIntegerField(choices=SKILL_LEVEL_CHOICES, null=True, blank=False)

    def __str__(self):  
        return self.name

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'


class Interest(models.Model):
    # user = model.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='interests')
    name = models.CharField(max_length= 128, null=True, blank=False)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):  
        return self.name 

    class Meta:
        verbose_name = 'Interest'
        verbose_name_plural = 'Interests'


class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experience')
    title = models.CharField(max_length=128, null=True, blank=False)
    worked_at = models.CharField(max_length=128, null=True, blank=False)
    duration = models.DurationField(default=timedelta(days=30))

    def __str__(self):  
        return self.title 

    class Meta:
        verbose_name = 'Experience'
        verbose_name_plural = 'Experience'

