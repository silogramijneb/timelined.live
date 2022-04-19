# For different views within main/app
from django.urls import path
from . import views
from dashboard import views as dviews

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", dviews.dashboard, name="dashboard"),
    path("dashboard/timeline/", dviews.timeline, name="timeline"),
]
