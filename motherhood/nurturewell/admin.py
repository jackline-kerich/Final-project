# nurturewell/admin.py
from django.contrib import admin
from .models import HealthMetrics, MindfulnessActivity, CommunityPost, EvidenceBasedInfo
from .models import (
    GuidedMeditation, Soundscape, MindfulMovement,
    GratitudeEntry, Affirmation, MoodEntry, MindfulnessChallenge
)
admin.site.register(HealthMetrics)
admin.site.register(MindfulnessActivity)
admin.site.register(GuidedMeditation)
admin.site.register(Soundscape)
admin.site.register(MindfulMovement)
admin.site.register(GratitudeEntry)
admin.site.register(Affirmation)
admin.site.register(MoodEntry)
admin.site.register(MindfulnessChallenge)
admin.site.register(CommunityPost)
admin.site.register(EvidenceBasedInfo)

