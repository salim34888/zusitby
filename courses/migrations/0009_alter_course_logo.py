# Generated by Django 5.1.1 on 2024-10-31 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_course_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='logo',
            field=models.FileField(default='images/1.png', upload_to='images'),
        ),
    ]
