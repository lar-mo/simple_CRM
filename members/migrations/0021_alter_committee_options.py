# Generated by Django 3.2.6 on 2021-09-10 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0020_auto_20210910_2237'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='committee',
            options={'ordering': ['person']},
        ),
    ]
