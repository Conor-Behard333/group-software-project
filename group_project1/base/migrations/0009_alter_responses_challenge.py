# Generated by Django 4.0.1 on 2022-02-25 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_challenges_lat_challenges_long'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responses',
            name='challenge',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='challenge_response', to='base.challenges'),
        ),
    ]
