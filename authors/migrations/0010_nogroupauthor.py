# Generated by Django 3.2 on 2021-05-01 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0009_rename_steamgroup_steamgroupname'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoGroupAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('steamid', models.CharField(max_length=30)),
            ],
        ),
    ]
