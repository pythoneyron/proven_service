from django.contrib import admin

from apps.contests.models import Team, Criteria, Contests, Assessment, NumberChanges, PlaceTaken, Penalty


@admin.register(PlaceTaken)
class PlaceTakenAdmin(admin.ModelAdmin):
    pass


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    pass


@admin.register(Contests)
class ContestsAdmin(admin.ModelAdmin):
    pass


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Penalty)
class PenaltyAdmin(admin.ModelAdmin):
    pass


@admin.register(NumberChanges)
class NumberChangesAdmin(admin.ModelAdmin):
    pass
