from django.contrib import admin
from .models import *


# Register your models here.
admin.site.Register(ServiceProvider)
admin.site.Register(Client)
admin.site.Register(thirdParty)
admin.site.Register(User)
admin.site.Register(Timeline)
admin.site.Register(Event)
admin.site.Register(Image)
admin.site.Register(Document)

