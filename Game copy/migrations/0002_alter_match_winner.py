# Generated by Django 4.2.14 on 2024-07-22 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_won', to=settings.AUTH_USER_MODEL),
        ),
    ]