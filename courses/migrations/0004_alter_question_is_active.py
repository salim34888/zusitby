# Generated by Django 5.1.1 on 2024-11-06 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_question_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
