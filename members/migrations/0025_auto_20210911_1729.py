# Generated by Django 3.2.6 on 2021-09-11 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0024_rename_brd_member_board_board_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='address',
        ),
        migrations.RemoveField(
            model_name='person',
            name='membership',
        ),
        migrations.AddField(
            model_name='membership',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member_address', to='members.address'),
        ),
        migrations.AddField(
            model_name='membership',
            name='person1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member_person1', to='members.person'),
        ),
        migrations.AddField(
            model_name='membership',
            name='person2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member_person2', to='members.person'),
        ),
        migrations.AlterField(
            model_name='board',
            name='board_member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='board_member', to='members.person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='partner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person', to='members.person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]
