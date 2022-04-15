from django.db import models
from django.db.models import Model

# Create your models here.
class ServiceProvider(models.Model):
    provider_name = models.CharField(max_length= 30)
    website = models.CharField(max_length= 50)

class Client(models.Model):
    client_name: models.CharField(max_length= 30)
    date_of_birth: models.DateField()

class thirdParty(models.Model) : 
    third_party_name = models.CharField(max_length= 30)
    website = models.CharField(max_length= 50)
    #category = models.Model()

class User(models.Model):

    #create user id
    user_id = = models.CharField(max_length = 16)

    #registering credentials
    user_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=9)

    #details of user specific to their use case
    serviceProvider_detail = models.OneToOneField(ServiceProvider)
    client_detail = models.OneToOneField(Client)
    thirdParty_detail = models.OneToOneField(thirdParty)

    #Data to show what timelines the user has specific permissions to view
    provider_permissions = models.OneToManyField(Timeline, on_delete=models.CASCADE)
    client_permissions = models.OneToManyField(Timeline, on_delete=models.CASCADE)
    thirdParty_permissions = models.OneToManyField(thirdParty, on_delete=models.CASCADE)

class Timeline(models.Model):
    #timeline id
    timeline_id = models.CharField(max_length = 16)
    #each Timeline contains many events and many users
    events = models.oneToManyField(Event, on_delete = models.CASCADE)
    users = models.oneToManyField(User, on_delete = models.CASCADE)


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

    #Who is allowed to edit the Timeline
    collaborators = models.oneToManyField(User, on_delete = models.CASCADE)

    pdf = models.oneToManyField(Document, on_delete = models.CASCADE)
    images = models.oneToManyField(Image, on_delete = models.CASCADE)

class Image(model.Model):
    image = models.ImageField(upload_to = 'uploads/')

class Document(models.Model):
    file = models.FileField(upload_to='files/', null=True, blank = True)

    def __str__(self):
        return self.name + ": " + str(self.filepath)
