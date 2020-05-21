from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from userprofile import views


urlpatterns = [

    path('profile/<str:username>/', views.ProfileView.as_view()),           #done
    path('profile/<str:username>/update/<uuid:pk>', views.ProfileUpdateView.as_view()),     #POP NOT WORKING

    path('project/list/<slug:tag_slug>/', views.ProjectListView.as_view(), name='project_list'),       #done
    path('project/details/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),    #done
    path('project/add/', views.ProjectAddView.as_view()),      #done
    
    path('search/profile/', views.ProfileSearchView.as_view()), 
    path('search/project/', views.ProjectSearchView.as_view()),
]


