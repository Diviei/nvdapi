#!/usr/bin/env python
import os
import sys
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nvdapi.settings")
import django
django.setup()
from xml_parser import *
from subprocess import call

# Download recent CVEs XML
os.system("wget -O /tmp/recent.zip http://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-Recent.xml.zip")
os.system("unzip -o /tmp/recent.zip -d /tmp/")
e = xml.etree.ElementTree.parse('/tmp/nvdcve-2.0-recent.xml').getroot()

for entry in e:
	process_entry(entry)

os.system("wget -O /tmp/modified.zip http://static.nvd.nist.gov/feeds/xml/cve/nvdcve-2.0-Modified.xml.zip")
os.system("unzip -o /tmp/modified.zip -d /tmp/")
e = xml.etree.ElementTree.parse('/tmp/nvdcve-2.0-modified.xml').getroot()

for entry in e:
	process_entry(entry)