# Generated by Django 3.2.6 on 2021-09-09 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0016_alter_needsreview_assignee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='needsreview',
            old_name='reason',
            new_name='component',
        ),
    ]