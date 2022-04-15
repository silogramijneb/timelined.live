from django.db import models
from django.db.models import Model


# Create your models here.

# Abstract class for the specific types to inherit
class User(models.Model):

    #create user id
    user_id = models.CharField(max_length = 16)

    #registering credentials
    user_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length = 64)
    provider_permissions = models.OneToOneField(ServiceProvider, on_delete=models.CASCADE)
    client_permissions = models.OneToOneField(Client, on_delete=models.CASCADE)
    thirdParty_permissions = models.OneToOneField(thirdParty, on_delete=models.CASCADE)
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE) # many users to one timeline
    class Meta:
        abstract = True

# ServiceProvider, Client, and thirdParty inherit attributes from User
class ServiceProvider(User):
    provider_name = models.CharField(max_length= 30)
    website = models.CharField(max_length= 50)

class Client(User):
    client_name = models.CharField(max_length= 30)
    date_of_birth = models.DateField()

class thirdParty(User) :
    third_party_name = models.CharField(max_length= 30)
    website = models.CharField(max_length= 50)
    #category = models.Model()

class Image(models.Model):
    image = models.ImageField(upload_to = 'uploads/')
    event = models.ForeignKey(Event) # many images to one event

class Event(models.Model):

    #status of event
    status = models.CharField(max_length = 30)

    #description of event
    description = models.CharField(max_length = 256)
    
    #location of event
    location = models.CharField(max_length = 100)

    #dates that are critical for time sensitivity of event
    date_created = models.DateField()
    deadline = models.DateField()
    date_modified = models.DateField()
    date_ended = models.DateField()

    timeline = models.ForeignKey(Timeline)  # many events to one timeline

    #Who is allowed to edit the Timeline
    #collaborators = models.oneToManyField(User, on_delete = models.CASCADE)

    #pdf = models.oneToManyField(Document, on_delete = models.CASCADE)
    #images = models.oneToManyField(Image, on_delete = models.CASCADE)

class Timeline(models.Model):
    #events = models.oneToManyField(Event, on_delete = models.CASCADE)
    #users = models.oneToManyField(User, on_delete = models.CASCADE)
    user = models.ForeignKey(User) # many timelines to one user

class Document(models.Model):
    file = models.FileField(upload_to='files/', null=True, blank = True)
    event = models.ForeignKey(Event) # many documents to one event

    def __str__(self):
        return self.name + ": " + str(self.filepath)
