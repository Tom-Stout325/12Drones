from django.db import models
from django.contrib.auth.models import User




class PilotProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=100)
    license_image = models.ImageField(upload_to='licenses/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class TrainingRecord(models.Model):
    profile = models.ForeignKey(PilotProfile, on_delete=models.CASCADE, related_name='trainings')
    training_name = models.CharField(max_length=200)
    training_date = models.DateField()

    class Meta:
        ordering = ['-training_date']

    def __str__(self):
        return f"{self.training_name} - {self.training_date}"
