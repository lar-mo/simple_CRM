# Generated by Django 3.2.6 on 2021-09-09 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_needsreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='needsreview',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Assigned', 'Assigned'), ('In-progress', 'In-progress'), ('Resolved', 'Resolved'), ('Closed', 'Closed')], default='Open', max_length=20),
        ),
    ]