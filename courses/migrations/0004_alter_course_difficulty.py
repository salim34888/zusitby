# Generated by Django 5.1.1 on 2024-10-30 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_course_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='difficulty',
            field=models.CharField(choices=[('EASY', 'EASY'), ('MIDDLE', 'MIDDLE'), ('HARD', 'HARD'), ('INSANE', 'INSANE')], default='EASY', max_length=6),
        ),
    ]