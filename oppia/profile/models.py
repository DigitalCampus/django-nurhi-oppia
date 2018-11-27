# oppia/profile/models.py

from django.contrib.auth.models import User
from django.db import models

from oppia.models import Participant


class UserProfile (models.Model):
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
    sex = models.CharField(max_length=50, default='')
    age = models.CharField(max_length=50, default='')
    phone_number = models.TextField(blank=True, null=True, default=None)

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
