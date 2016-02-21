from django.core.management.base import BaseCommand, CommandError
from _utils import *
import os

class Command(BaseCommand):
    help = 'Get data from NVD from the beginning or defined year'

    def add_arguments(self, parser):
        parser.add_argument('-y', type=int, help="Initial year to start processing")

    def handle(self, *args, **options):
        initial_year = options.get('y', 2002)
        
        try:
            initial_year = int(initial_year)
        except:
            initial_year = 2002

        final_year = 2016
        for i in range(initial_year, final_year):
            os.system("wget -O /tmp/aux.zip http://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-%i.xml.zip" % i)
            os.system("unzip -o /tmp/aux.zip -d /tmp/")
            e = xml.etree.ElementTree.parse('/tmp/nvdcve-2.0-%i.xml' % i).getroot()
            for entry in e:
                process_entry(entry)

        self.stdout.write('Process finished')