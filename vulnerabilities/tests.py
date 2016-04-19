from django.test import TestCase
from vulnerabilities.models import *
from django.core.management import call_command

# Create your tests here.
class CommandsTestCase(TestCase):
    def setUp(self):
        pass

    def test_recent_nvd(self):
        call_command('nvdrecent')

    def test_modified_nvd(self):
        call_command('nvdmodified')