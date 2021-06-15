from django.db import models


class Author(models.Model):
    nicname = models.CharField(max_length=255, help_text="Enter the author's Steam profile name")
    profile_url = models.URLField()
    avatar = models.URLField()
    number_of_followers = models.IntegerField()
    workshop_submissions = models.IntegerField()
    coop_maps = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['nicname', '-number_of_followers']),
        ]

    def __str__(self):
        return self.nicname


class NoGroupAuthor(models.Model):
    steamid = models.CharField(max_length=30)

    def __str__(self):
        return self.steamid


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

    def __str__(self):
        return self.group_name


class UpdateDate(models.Model):
    model_name = models.CharField(max_length=20)
    timestamp = models.DateTimeField()

    def date(self):
        return self.timestamp.strftime('%b %d, %Y')

    def __str__(self):
        return self.model_name