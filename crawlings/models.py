from django.db import models

# Create your models here.
class Jusik(models.Model):
    company = models.CharField(max_length=50)
    company_code = models.CharField(max_length=50)
    comment = models.TextField()
    created_at = models.CharField(max_length=50)