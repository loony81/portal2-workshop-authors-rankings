# Generated by Django 3.2 on 2021-05-01 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0007_authortemp'),
    ]

    operations = [
        migrations.CreateModel(
            name='SteamGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=200)),
            ],
        ),
    ]