from django.db import models
from django.utils import timezone
from django import forms

from main.models import Timeline, Document

# Create your models here.
class TimelineEvent(models.Model):
    class Meta:
        db_table = "TimelineEvent"
    
    title = models.CharField(max_length=32)
    #event_types = (
        ('0', 'meeting'),
        ('1', 'schedule_appointment'),
        ('2', 'repair'),
        ('3', 'maintainenance'),
        ('4', 'verification'),
        ('5', 'document_upload'),
        ('6', 'inspection'),
        ('7', 'check_up'),
        ('8', 'contact'),
        ('9', 'custom'),
    )
    #event_type = forms.ChoiceField(choices=event_types)
    description = models.TextField()
    #status_codes = (
        ('0', 'unscheduled'), 
        ('1', 'scheduled'),
        ('2', 'completed'),
        ('3', 'in_progress'),
        ('4', 'upcoming'),
        ('5', 'overdue'),
    )
    #status = forms.ChoiceField(choices=status_codes)
    location = models.CharField(max_length=64)
    date_created = models.DateField(auto_now_add=True)
    date_last_modified = models.DateField(auto_now=True)
    date_completed = models.DateField(null=True)
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    file_upload = models.OneToOneField(Document, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return {
            "title": self.title,
            "event_type": self.event_type,
            "description": self.description,
            "status": self.status,
            "location": self.location,
            "history": {
                "date_created": self.date_created,
                "date_last_modified": self.date_last_modified,
                "date_completed": self.date_completed,
            },
            "timeline": self.timeline,
            "file_upload": self.file_upload,
        }
