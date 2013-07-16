from django.db import models

# Create your models here.

class PlivoSubAccount(models.Model):
    name = models.CharField(max_length=40)
    enabled = models.BooleanField(default=True)
    auth_id = models.CharField(max_length=30)
    auth_token = models.CharField(max_length=50)

    def __unicode__(self):
        return u"%s" % self.name


