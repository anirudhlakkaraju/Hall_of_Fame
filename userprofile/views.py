from .filters import DynamicSearchFilters
from .models import Profile, Project, Skill, Interest, Experience
from .serializers import ProfileDetailSerializer, ProfileUpdateSerializer, ProjectSerializer, InterestSerializer, SkillSerializer, ExperienceSerializer

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView, Response


class ProjectListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    
    def get(self, request, tag_slug):
        ''' Returns list of projects having the same tag. '''

        projects = Project.objects.filter(tags__slug=tag_slug)
        
        if not projects:
            return Response("", status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(projects, many=True)
        context = {
            "projects" : serializer.data
        }
        return Response(data=context)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(self, request, slug):
        ''' Returns details of a project. '''
        project = Project.objects.filter(slug=slug)

        if not project:
            return Response("", status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project, many=True)
        context = {
            "project" : serializer.data
        }
        return Response(data=context)


class ProjectAddView(CreateAPIView):
    # prepopulate profile field with current user uuid
    permission_classes = [IsAuthenticated, ]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProfileUpdateView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer


class ProfileView(APIView):
        permission_classes = [IsAuthenticatedOrReadOnly, ]

        def get(self, request, username):
            user = User.objects.filter(username=username).first()

            if not user:
                return Response("", status=status.HTTP_404_NOT_FOUND)

            profile = user.profile.all()
            if not profile:
                return Response("", status=status.HTTP_404_NOT_FOUND)

            profile = profile[0]
            profile_serializer = ProfileDetailSerializer(profile)
            context = {
                "profile" : profile_serializer.data,
            }
            return Response(data=context)


class ProfileSearchView(generics.ListCreateAPIView):

        # Filters search fields for the argument passed
        search_fields = ['user__username', 'college', 'skills__name', 
                        'experience__title', ]
        
        filter_fields = ['title', 'tags__name', 'abstract', ]
        filter_backends = (filters.SearchFilter, DjangoFilterBackend, DynamicSearchFilters, )
        queryset = Profile.objects.all()
        serializer_class = ProfileDetailSerializer


class ProjectSearchView(generics.ListCreateAPIView):

        # Filters search fields for the argument passed
        filter_backends = (filters.SearchFilter, DjangoFilterBackend, DynamicSearchFilters, )
        search_fields = ['title', 'tags__name', 'abstract', ]
        filter_fields = ['title', 'tags__name', 'abstract', ]
        queryset = Project.objects.all()
        serializer_class = ProjectSerializer

