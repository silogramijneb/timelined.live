from django.db import models

# Create your models here.
class User(models.Model):
    user_name  = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length= 9)
    provider_permissions = models.OneToOneField(ServiceProvider)
    client_permissions = models.OneToOneField(Client)
    thirdParty_permissions = models.OneToOneField(thirdParty)

class ServiceProvider(models.Model):
    provider_name = models.CharField(max_length= 30)
    website = models.CharField(max_length= 50)

class Client(models.Model):
    client_name: models.CharField(max_length= 30)
    date_of_birth: models.DateField()

class thirdParty(models.Model) : 
    third_party_name = models.CharField(max_length= 30)
    website = models.CharField(max_length= 50)
    category = models.Model()
