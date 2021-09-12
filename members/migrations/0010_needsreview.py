# Generated by Django 3.2.6 on 2021-09-09 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_auto_20210909_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='NeedsReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('reason', models.CharField(choices=[('Name', 'Name'), ('Address', 'Address'), ('Partner', 'Partner'), ('Council Membership', 'Council Membership'), ('Board Membership', 'Board Membership'), ('Committee Membeship', 'Committee Membeship')], max_length=30)),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Assigned', 'Assigned'), ('In-progress', 'In-progress'), ('Resolved', 'Resolved'), ('Closed', 'Closed')], max_length=20, unique=True)),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to='members.person')),
            ],
        ),
    ]