from django.urls import path
from . import views

urlpatterns = [
    path("", views.kb_finaissist, name="kb_finaissist"),
]
