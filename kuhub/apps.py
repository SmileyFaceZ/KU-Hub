"""
import application configuration from django.
"""
from django.apps import AppConfig


class KuHubConfig(AppConfig):
    """KU-Hub Configuration."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "kuhub"
