# Generated by Django 5.1.1 on 2024-10-31 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_course_difficulty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='difficulty',
            field=models.CharField(choices=[('EAS', 'EASY'), ('MID', 'MIDDLE'), ('HARD', 'HARD'), ('INS', 'INSANE')], default='EAS', max_length=4),
        ),
    ]