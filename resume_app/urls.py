from django.urls import path
from .views import upload_resume

urlpatterns = [
    path('api/upload_resume/',upload_resume,name='upload_resume')
]
