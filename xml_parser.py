#!/usr/bin/env python
import os
import sys
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nvdapi.settings")
import django
django.setup()
from vulnerabilities.models import *

import xml.etree.ElementTree
import datetime
from django.utils import timezone
from django.conf import settings

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
    published_on = timezone.make_aware(get_published_datetime(entry), timezone.get_default_timezone())
    modified_on = timezone.make_aware(get_last_modified_datetime(entry), timezone.get_default_timezone())
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

    if created:
        print "CREATED %s" % vuln.cve

    if not created and vuln.modified_on != modified_on:
        vuln.modified_on = modified_on
        vuln.description = summary
        vuln.score = score
        vuln.access_vector = access_vector
        vuln.access_complexity = access_complexity
        vuln.authentication = authentication
        vuln.confidentiality_impact = confidentiality_impact
        vuln.integrity_impact = integrity_impact
        vuln.availability_impact = availability_impact
        vuln.save()
        print "UPDATED %s" % vuln.cve

    def clean_cpe(string):
        return string.replace("_"," ").replace("-","")

    #Process CPEs
    for cpe in cpes:
        aux = cpe.replace("cpe:/","").split(":")

        try:
            version = aux[3]
        except IndexError:
            version = None

        try:
            product, created = Product.objects.get_or_create(cpe=cpe, defaults={
                            "vendor":clean_cpe(aux[1]),
                            "name":clean_cpe(aux[2]),
                            "type":clean_cpe(aux[0]),
                            "version":version
                            })
            vuln.product.add(product)
        except:
            continue

    #Process references
    for url in references:
        VulnerabilitySource.objects.get_or_create(vulnerability=vuln, url=url)

    print vuln
