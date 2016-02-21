from django.core.management.base import BaseCommand, CommandError
from _utils import *
import os

class Command(BaseCommand):
    help = 'Get recent vulnerabilities from NVD'

    def handle(self, *args, **options):
        os.system("wget -O /tmp/recent.zip http://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-Recent.xml.zip")
        os.system("unzip -o /tmp/recent.zip -d /tmp/")
        e = xml.etree.ElementTree.parse('/tmp/nvdcve-2.0-recent.xml').getroot()

        for entry in e:
            process_entry(entry)

        self.stdout.write('Process finished')