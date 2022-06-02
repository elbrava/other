# Generated by Django 4.0.4 on 2022-05-30 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sara', '0002_rooms'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='condition',
            field=models.CharField(default='', max_length=455),
        ),
        migrations.AddField(
            model_name='rooms',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rooms',
            name='empty',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='rooms',
            name='full',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rooms',
            name='in_session',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rooms',
            name='max_users',
            field=models.IntegerField(default=5),
        ),
    ]
