# Generated by Django 3.2.6 on 2021-09-11 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0029_alter_membership_person1'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membership',
            options={'ordering': ['level', 'person1__last_name']},
        ),
        migrations.RemoveField(
            model_name='membership',
            name='description',
        ),
    ]
