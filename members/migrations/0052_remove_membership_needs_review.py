# Generated by Django 3.2.6 on 2021-09-11 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0051_alter_needsreview_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='needs_review',
        ),
    ]
