# Generated by Django 4.1.7 on 2023-05-05 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_course_prof'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_lession',
            name='file',
            field=models.FileField(null=True, upload_to='files/'),
        ),
    ]