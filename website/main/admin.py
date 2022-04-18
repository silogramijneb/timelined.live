from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(ServiceProvider)
admin.site.register(Client)
admin.site.register(ThirdParty)
admin.site.register(UserTimeline)
admin.site.register(Timeline)
admin.site.register(Event)
#admin.site.register(Image)
admin.site.register(Document)

