# Generated by Django 3.2.6 on 2021-10-03 16:43

from django.db import migrations, models
import django.db.models.deletion
import members.models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('address_1', models.CharField(max_length=100)),
                ('address_2', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District Of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=20)),
                ('postal_code', models.CharField(max_length=20)),
                ('country', models.CharField(default='US', max_length=30)),
            ],
            options={
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('President', 'President'), ('Vice President', 'Vice President'), ('Secretary', 'Secretary'), ('Treasurer', 'Treasurer'), ('Past President', 'Past President'), ('Committee', 'Committee')], max_length=20)),
                ('committees', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Advisory', 'Advisory'), ('Archives', 'Archives'), ('Book Club', 'Book Club'), ('Communication', 'Communications'), ('Day Trips', 'Day Trips'), ('Memberships', 'Memberships'), ('Membership Development', 'Membership Development'), ('Directory', 'Directory'), ('Photographer', 'Photographer'), ('Programs', 'Programs'), ('Special Events', 'Special Events'), ('Hopitality: Beverages', 'Hopitality: Beverages'), ('Hopitality: Food', 'Hopitality: Food'), ('Hopitality: Greeter', 'Hopitality: Greeter'), ('Hopitality: RSVPs/Name Tags', 'Hopitality: RSVPs/Name Tags'), ('Travel', 'Travel'), ('Board of Trustees Council Liaison', 'Board of Trustees Council Liaison'), ('Council Coordinator', 'Council Coordinator')], max_length=50)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('Supporter', 'Supporter'), ('Contributor', 'Contributor'), ('Advocate', 'Advocate'), ('Honorary', 'Honorary'), ('PAM staff', 'PAM staff')], default='Supporter', max_length=20)),
                ('expiration', models.DateField(blank=True, default=members.models.one_year_from_today, null=True)),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=10)),
                ('notes', models.CharField(blank=True, max_length=300)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member_address', to='members.address')),
            ],
            options={
                'ordering': ['level', 'person1__last_name'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('byline', models.CharField(blank=True, max_length=100)),
                ('nickname', models.CharField(blank=True, max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('notes', models.CharField(blank=True, max_length=300)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address', to='members.address')),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='NeedsReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=100, null=True)),
                ('description', models.TextField(null=True)),
                ('component', models.CharField(choices=[('Name', 'Name'), ('Address', 'Address'), ('Email', 'Email'), ('Phone Number', 'Phone Number'), ('Partner', 'Partner'), ('Council Membership', 'Council Membership'), ('Board Membership', 'Board Membership'), ('Committee Membership', 'Committee Membership')], max_length=30)),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('ASSIGNED', 'Assigned'), ('CLOSED', 'Closed')], default='OPEN', max_length=20)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to='members.board')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nr_member', to='members.membership')),
                ('person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nr_person', to='members.person')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='person1',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person_1', to='members.person'),
        ),
        migrations.AddField(
            model_name='membership',
            name='person2',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person_2', to='members.person'),
        ),
        migrations.AddField(
            model_name='board',
            name='person1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='board_member', to='members.person'),
        ),
    ]
