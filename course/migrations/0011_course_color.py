# Generated by Django 4.1.7 on 2023-05-05 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_user_lession_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='color',
            field=models.CharField(default='#2FBCD2', max_length=41),
            preserve_default=False,
        ),
    ]
