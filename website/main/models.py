from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# TimelineUser is a profile of a standard user.
# Contains Django's built in user model. Contains information pertaining strictly to authentication.
# Other fields are characterstics of one's profile that are necessay but not needed for authentication
class Profile(User):
    class Meta:
        db_table = 'TimelineUser'

    phone = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

# ServiceProvider, Client, and thirdParty inherit attributes from User
class ServiceProvider(Profile):
    class Meta:
        db_table = 'ServiceProvider'

    provider_name = models.CharField(max_length= 30)
    website = models.CharField(max_length= 50)

    def __str__(self):
        return "(" + self.provider_name + ") " + self.first_name + " " + self.last_name
    
class Client(Profile):
    class Meta:
        db_table = 'Client'

    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class ThirdParty(Profile) :
    third_party_name = models.CharField(max_length= 30)
    website = models.CharField(max_length= 50)
    #category = models.Model()

    def __str__(self):
        return  self.third_party_name

class Document(models.Model):
    id = models.BigIntegerField(primary_key=True)
    file = models.FileField(upload_to='media/', null=True, blank = True)

    def __str__(self):
        return self.filename + ": " + str(self.filepath)

class Timeline(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length = 50)
    # events = models.ForeignKey(Event, on_delete = models.CASCADE, null=True)
    # users = models.ForeignKey(User, on_delete = models.CASCADE)
    #user = models.ForeignKey(User, on_delete=models.PROTECT) # many timelines to one user
    #user.many_to_one = True

    def __str__(self):
        return self.name
    
    def getId(self):
        return self.id

class Event(models.Model):

    id = models.BigIntegerField(primary_key=True)

    index = models.IntegerField()

    #event name
    name = models.CharField(max_length = 50)

    #status of event
    status = models.CharField(max_length = 30)

    #description of event
    description = models.CharField(max_length = 256)
    
    #location of event
    location = models.CharField(max_length = 100)

    #dates that are critical for time sensitivity of event
    start_date = models.DateField()
    end_date = models.DateField()
    date_modified = models.DateField(auto_now=True)
    date_ended = models.DateField(null=True)

    timeline = models.ForeignKey(Timeline, on_delete = models.CASCADE)

    # timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)  # many events to one timeline

    #Who is allowed to edit the Timeline
    #collaborators = models.oneToManyField(User, on_delete = models.CASCADE)

    file = models.OneToOneField(Document, on_delete = models.CASCADE, null=True)

    def __str__(self):
        return self.name


class UserTimeline(models.Model):
    class Meta:
        db_table = 'Timeline<->User'

    # third_party = models.ForeignKey(ThirdParty, null=True, on_delete=models.PROTECT)
    service_provider_id = models.BigIntegerField()
    client_id = models.BigIntegerField()
    timeline_id = models.BigIntegerField()
    third_party_id = models.BigIntegerField()

    def __str__(self):
        return self.service_provider + ": " + self.client
