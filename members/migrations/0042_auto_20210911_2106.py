# Generated by Django 3.2.6 on 2021-09-11 21:06

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0041_auto_20210911_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='committees',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Advisory', 'Advisory'), ('Archives', 'Archives'), ('Book Club', 'Book Club'), ('Communications', 'Communications'), ('Day Trips', 'Day Trips'), ('Memberships', 'Memberships'), ('Membership Development', 'Membership Development'), ('Directory', 'Directory'), ('Photographer', 'Photographer'), ('Programs', 'Programs'), ('Special Events', 'Special Events'), ([('Hopitality: Beverages', 'Beverages'), ('Hopitality: Food', 'Food'), ('Hopitality: Greeter', 'Greeter'), ('Hopitality: RSVP and Name Tags', 'RSVPs/Name Tags')], [('Hopitality: Beverages', 'Beverages'), ('Hopitality: Food', 'Food'), ('Hopitality: Greeter', 'Greeter'), ('Hopitality: RSVP and Name Tags', 'RSVPs/Name Tags')]), ('Travel', 'Travel'), ('Board of Trustees Council Liaison', 'Board of Trustees Council Liaison'), ('Council Coordinator', 'Council Coordinator')], max_length=40),
        ),
        migrations.AlterField(
            model_name='board',
            name='title',
            field=models.CharField(choices=[('President', 'President'), ('Vice President', 'Vice President'), ('Secretary', 'Secretary'), ('Treasurer', 'Treasurer'), ('Past President', 'Past President'), ('Commitee', 'Commitee')], max_length=20),
        ),
        migrations.AlterField(
            model_name='membership',
            name='level',
            field=models.CharField(choices=[('Supporter', 'Supporter'), ('Contributor', 'Contributor'), ('Advocate', 'Advocate'), ('Honorary', 'Honorary'), ('PAM staff', 'PAM staff')], default='SUPPORTER', max_length=20),
        ),
        migrations.AlterField(
            model_name='membership',
            name='status',
            field=models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='ACTIVE', max_length=10),
        ),
        migrations.AlterField(
            model_name='needsreview',
            name='component',
            field=models.CharField(choices=[('Name', 'Name'), ('Address', 'Address'), ('Email', 'Email'), ('Phone Number', 'Phone Number'), ('Partner', 'Partner'), ('Council Membership', 'Council Membership'), ('Board Membership', 'Board Membership'), ('Committee Membeship', 'Committee Membeship')], max_length=30),
        ),
    ]