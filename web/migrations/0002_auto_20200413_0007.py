# Generated by Django 2.2.11 on 2020-04-12 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='update',
            options={'ordering': ['-created']},
        ),
    ]
