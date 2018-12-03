# oppia/profile/models.py

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from oppia.models import Participant


class UserProfile (models.Model):
    
    AGE_RANGE = [
        ('under_18', _(u'under 18')),
        ('18_25', _(u'18-24')),
        ('25_35', _(u'25-34')),
        ('35_50', _(u'35-50')),
        ('over_50', _(u'over 50')),
        ('none', _(u'Prefer not to say')),
    ]
    GENDER = [
        ('female', _(u'Female')),
        ('male', _(u'Male')),
        ('none', _(u'Prefer not to say')),
    ]
    ROLE = [
        ('fpprovider', _(u'FP provider')),
        ('fpmanager', _(u'FP manager/supervisor')),
        ('other', _(u'Other')),
    ]
    
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True, default=None)
    can_upload = models.BooleanField(default=False)
    job_title = models.TextField(blank=True, null=True, default=None)
    organisation = models.TextField(blank=True, null=True, default=None)
    phoneno = models.CharField(max_length=50, default='')
    currently_working_facility = models.CharField(max_length=50, default='')
    staff_type = models.CharField(max_length=50, default='')
    nurhi_sponsor_training = models.CharField(max_length=50, default='')
    highest_education_level = models.CharField(max_length=50, default='')
    fp_methods_provided = models.TextField(null=True, blank=True, default=None)
    religion = models.CharField(max_length=50, default='')
    sex =models.CharField(max_length=50, choices=GENDER, default='none')
    age = models.CharField(max_length=50, default='')
    phone_number = models.TextField(blank=True, null=True, default=None)

    age_range = models.CharField(max_length=50, choices=AGE_RANGE, default='none')
    role = models.CharField(max_length=50, choices=ROLE, default='none')
    location = models.TextField(blank=True, null=True, default=None)
    
    def get_can_upload(self):
        if self.user.is_staff:
            return True
        return self.can_upload

    def get_can_upload_activitylog(self):
        if self.user.is_staff:
            return True
        return False

    def is_student_only(self):
        if self.user.is_staff:
            return False
        teach = Participant.objects.filter(user=self.user, role=Participant.TEACHER).count()
        if teach > 0:
            return False
        else:
            return True

    def is_teacher_only(self):
        if self.user.is_staff:
            return False
        teach = Participant.objects.filter(user=self.user, role=Participant.TEACHER).count()
        if teach > 0:
            return True
        else:
            return False
