from django.contrib import admin

from polls.models import Poll, Vote, Choice



class ChoiceInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = Choice
    extra = 1

class PollInLine(admin.TabularInline):
    model = Poll
    extra = 1

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ["poll_text", "pub_date", "created_at"]
    search_fields = ["poll_text"]
    list_filter = ['created_at', 'pub_date']
    date_hierarchy = "pub_date"
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["choice_text", "poll", 'created_at', 'updated_at']
    search_fields = ["choice_text", "poll__poll_text"]
    autocomplete_fields = ["poll"]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["choice", "poll", "user", 'created_at']
    search_fields = ["choice__choice_text", "poll__poll_text", "user__username"]
    autocomplete_fields = ["choice", "poll", "user"]