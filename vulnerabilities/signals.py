from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, m2m_changed
from vulnerabilities.models import Vulnerability
from django.conf import settings