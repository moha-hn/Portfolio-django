from django.contrib import admin
from .models import Project, Education, Talk


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'order']
    list_editable = ['featured', 'order']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'year_start', 'year_end', 'order']
    list_editable = ['order']


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_display = ['title', 'event', 'date', 'order']
    list_editable = ['order']