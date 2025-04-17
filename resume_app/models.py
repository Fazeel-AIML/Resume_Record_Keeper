from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=255)
    current_designation = models.CharField(max_length=255)
    experiences = models.IntegerField()  # Number of experiences
    skills = models.TextField()  # Comma-separated string of skills
    file = models.FileField(upload_to='resumes/')
    summary = models.TextField(null=True, blank=True)  # Summary of the resume
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}'s Resume"