from django.db import models


class Author(models.Model):
    nicname = models.CharField(max_length=255)
    profile_url = models.CharField(max_length=2083)
    avatar = models.CharField(max_length=2083)
    number_of_followers = models.IntegerField()
    workshop_submissions = models.IntegerField()
    coop_maps = models.IntegerField()


class AuthorTemp(models.Model):
    nicname = models.CharField(max_length=255)
    profile_url = models.CharField(max_length=2083)
    avatar = models.CharField(max_length=2083)
    number_of_followers = models.IntegerField()
    workshop_submissions = models.IntegerField()
    coop_maps = models.IntegerField()


class Steamid(models.Model):
    steamid = models.CharField(max_length=30)


class SteamGroupName(models.Model):
    group_name = models.CharField(max_length=200)

