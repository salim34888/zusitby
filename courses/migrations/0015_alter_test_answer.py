# Generated by Django 5.1.1 on 2024-10-11 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_alter_content_content_type_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='answer',
            field=models.CharField(max_length=255),
        ),
    ]