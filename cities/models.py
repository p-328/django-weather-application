from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL
# Create your models here.


class City(models.Model):
    id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255)
    country_or_state = models.CharField(max_length=255)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "%s, %s" % (self.city_name, self.country_or_state)

    class Meta:
        db_table = 'cities'
