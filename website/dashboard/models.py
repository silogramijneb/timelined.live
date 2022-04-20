from django.db import models
from django.utils import timezone

# Create your models here.
class TimelineEvent(models.Model):

    class Type(models.IntegerChoices):
        MEETING = 0
        SCHEDULE_APPOINTMENT = 1
        REPAIR = 2
        MAINTAINANCE = 3
        VERIFICATION = 4
        VIEWING = 5
        CHECK_UP = 6
        DOCUMENT_UPLOAD = 7
    
    class Status(models.IntegerChoices):
        UNSCHEDULED = 0
        SCHEDULED = 1
        COMPLETED = 2
        UPCOMING = 3

    title = models.CharField(max_length=32)
    event_type = models.IntegerField(choices=Type.choices)
    description = models.CharField(max_length=240)
    status = models.IntegerField(choices=Status.choices)
    dependent_on  = models.CharField(max_length=32)
