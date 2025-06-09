from django.db import models

class SurahProgress(models.Model):
    current_ayah = models.IntegerField(default=1)
    completed_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Ayah {self.current_ayah} - Completed {self.completed_count} times"

class AyahAssignment(models.Model):
    ayah_number = models.IntegerField(unique=True)

    def __str__(self):
        return f"آیه شماره {self.ayah_number}"
