from django.contrib import admin

from .models import Survey
from  polls.admin import PollInLine

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ["title", "description", 'created_at']
    search_fields = ["title"]
    inlines = [PollInLine]