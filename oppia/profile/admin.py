# oppia/profile/admin.py

from django.contrib import admin

from oppia.profile.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'can_upload', 'about', 'job_title', 'organisation','phoneno',
                    'currently_working_facility',
                    'staff_type',
                    'nurhi_sponsor_training',
                    'fp_methods_provided',
                    'highest_education_level',
                    'religion',
                    'sex',
                    'age',)

admin.site.register(UserProfile, UserProfileAdmin)
