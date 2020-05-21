from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Project, Skill, Interest, Experience

class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


admin.site.register(Profile)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Skill)
admin.site.register(Interest)
admin.site.register(Experience)
