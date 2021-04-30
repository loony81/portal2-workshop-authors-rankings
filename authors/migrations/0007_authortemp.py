# Generated by Django 3.2 on 2021-04-30 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0006_steamid'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nicname', models.CharField(max_length=255)),
                ('profile_url', models.CharField(max_length=2083)),
                ('avatar', models.CharField(max_length=2083)),
                ('number_of_followers', models.IntegerField()),
                ('workshop_submissions', models.IntegerField()),
                ('coop_maps', models.IntegerField()),
            ],
        ),
    ]
