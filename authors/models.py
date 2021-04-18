from django.db import models


class Author(models.Model):
    nicname = models.CharField(max_length=255)
    profile_url = models.CharField(max_length=2083)
    avatar = models.CharField(max_length=2083)
    loc_country_code = models.CharField(max_length=10, default='-')
    number_of_followers = models.IntegerField()
    workshop_submissions = models.IntegerField()

