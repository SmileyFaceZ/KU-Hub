# Generated by Django 4.2.4 on 2023-11-09 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from kuhub.models import Profile
from django.contrib.auth.models import User


def create_user_profiles(apps, schema_editor):
    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)


def create_user_profile_reverse(apps, schema_editor):
    Profile = apps.get_model('kuhub', 'Profile')
    Profile.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kuhub', '0006_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biography', models.TextField(blank=True)),
                (
                    'user',
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(create_user_profiles, reverse_code=create_user_profile_reverse)
    ]