# Generated by Django 5.1.1 on 2024-10-11 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_useranswer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserAnswer',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
