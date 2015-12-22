#!/usr/bin/env python
import os
import sys
import time
from nvd_parser import NVD_PARSER
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nvdapi.settings")
import django
django.setup()
from vulnerabilities.models import *


clear = lambda: os.system('clear')
year = int(sys.argv[1])
fails = 0

def processCVE(CVE):
	global fails

	parser = NVD_PARSER(CVE)
	parser.parse()

	if parser.validCVE and parser.cvss:
		#Create vulnerability
		vuln, created = Vulnerability.objects.get_or_create(cve=CVE, defaults={
							"released_on":parser.release_date, "description":parser.description,
							"cvss":parser.cvss})

		#Process CPEs
		for cpe in parser.cpes:
			aux = cpe.replace("cpe:/","").split(":")
			product, created = Product.objects.get_or_create(vendor=aux[1].replace("_"," "), name=aux[2].replace("_"," "), defaults={"type":aux[0], })
			try:
				version = aux[3]
			except Exception, e:
				version = ""
			try:
				product_version, created = ProductVersion.objects.get_or_create(product=product, version=version)
			except Exception, e:
				product_version = ProductVersion.objects.get(product=product, version=version)
			vuln.product_version.add(product_version)

		#Process references
		for url in parser.references:
			VulnerabilitySource.objects.get_or_create(vulnerability=vuln, url=url)
	else:
		fails = fails + 1
		time.sleep(5)
		if parser.timeout:
			cves.append(CVE)
		else:
			print "Invalid CVE"

def worker():
	aux = True
	global fails
	while aux:
		clear()
		print "Fails %i" % fails
		try:
			cve = cves.pop(0)
			processCVE(cve)
		except Exception, e:
			fails = fails + 1
			time.sleep(5)
			cves.append(CVE)

cves = []
threads = []

for i in range(1, 10000):
	CVE = "CVE-%i-%s" % (year, str(i).zfill(4))
	cves.append(CVE)

worker()