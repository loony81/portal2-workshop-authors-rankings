# Generated by Django 3.2 on 2021-05-30 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0014_alter_author_nicname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='avatar',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='author',
            name='profile_url',
            field=models.URLField(),
        ),
    ]
