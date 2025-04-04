from django.db import models

# Create your models here.
class Jusik(models.Model):
    company = models.CharField(max_length=50)
    copany_code = models.CharField(max_length=50)
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)