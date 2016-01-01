#!/usr/bin/env python
import os
import sys
import time
from nvd_parser import NVD_PARSER
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nvdapi.settings")
import django
django.setup()
from vulnerabilities.models import *

import xml.etree.ElementTree
import datetime
from django.utils import timezone
import twitter
from django.conf import settings

api = twitter.Api(consumer_key = settings.TWITTER_CONSUMER_KEY,
                    consumer_secret = settings.TWITTER_CONSUMER_SECRET,
                    access_token_key = settings.TWITTER_ACCESS_TOKEN,
					access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET)

def get_cve(entry):
	return entry.attrib.get("id")
def get_published_datetime(entry):
	for childs in entry:
		if "published-datetime" in childs.tag:
			return datetime.datetime.strptime(childs.text[:-10], "%Y-%m-%dT%H:%M:%S")
def get_last_modified_datetime(entry):
	for childs in entry:
		if "last-modified-datetime" in childs.tag:
			return datetime.datetime.strptime(childs.text[:-10], "%Y-%m-%dT%H:%M:%S")
def get_summary(entry):
	for childs in entry:
		if "summary" in childs.tag:
			return childs.text
def get_score(entry):
	for child in entry:
		if "cvss" in child.tag:
			base_metrics = child[0] #base_metrics
			for aux in base_metrics:
				if "score" in aux.tag:
					return float(aux.text)
	return float(0)
def get_cvss_value(entry, value):
	for child in entry:
		if "cvss" in child.tag:
			base_metrics = child[0] #base_metrics
			for aux in base_metrics:
				if value in aux.tag:
					return aux.text
def get_cpes_affected(entry):
	cpes = []
	for child in entry:
		if "vulnerable-software-list" in child.tag:
			vulnerable_software = child
			for cpe in vulnerable_software:
				cpes.append(cpe.text)
	return cpes
def get_references(entry):
	references = []
	for child in entry:
		if "references" in child.tag:
			for aux in child:
				if "reference" in aux.tag:
					references.append(aux.attrib.get("href"))
	return references
def process_entry(entry):
	cve = get_cve(entry)
	published_on = get_published_datetime(entry)
	modified_on = get_last_modified_datetime(entry)
	summary = get_summary(entry)
	score = get_score(entry)
	access_vector = get_cvss_value(entry, 'access-vector')
	access_complexity = get_cvss_value(entry, 'access-complexity')
	authentication = get_cvss_value(entry, 'authentication')
	confidentiality_impact = get_cvss_value(entry, 'confidentiality-impact')
	integrity_impact = get_cvss_value(entry, 'integrity-impact')
	availability_impact = get_cvss_value(entry, 'availability-impact')
	cpes = get_cpes_affected(entry)
	references = get_references(entry)

	vuln, created = Vulnerability.objects.get_or_create(cve=cve, defaults={
							"released_on":published_on, 
							"modified_on":modified_on, 
							"description":summary,
							"score":score,
							"access_vector":access_vector,
							"access_complexity":access_complexity,
							"authentication":authentication,
							"confidentiality_impact":confidentiality_impact,
							"integrity_impact":integrity_impact,
							"availability_impact":availability_impact})

	count_before = vuln.product_version.count()

	#Process CPEs
	for cpe in cpes:
		aux = cpe.replace("cpe:/","").split(":")
		
		try:
			product, created = Product.objects.get_or_create(vendor=aux[1].replace("_"," "), 
							name=aux[2].replace("_"," "), 
							defaults={"type":aux[0], })
		except Exception, e:
			continue

		try:
			version = aux[3]
		except Exception, e:
			version = ""
		try:
			product_version, created = ProductVersion.objects.get_or_create(product=product, version=version)
		except Exception, e:
			product_version = ProductVersion.objects.get(product=product, version=version)
		vuln.product_version.add(product_version)

	count_after = vuln.product_version.count()
	if count_after > count_before:
		products = [x.product.name for x in vuln.product_version.all()]
		products = list(set(products))
		link = "https://web.nvd.nist.gov/view/vuln/detail?vulnId=%s" % vuln.cve

		tweet = []
		tweet.append(vuln.cve)
		tweet.append("(%s)" % ', '.join(products))
		tweet.append(link)
		tweet = " ".join(tweet)
		status = api.PostUpdate(tweet)

	#Process references
	for url in references:
		VulnerabilitySource.objects.get_or_create(vulnerability=vuln, url=url)

	print vuln
# for i in range(14,16):
# 	e = xml.etree.ElementTree.parse('nvdcve-2.0-20%s.xml' % format(i,'02')).getroot()
# 	for entry in e:
# 		process_entry(entry)