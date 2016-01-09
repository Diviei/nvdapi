from django.db import models

class Product(models.Model):
	type = models.CharField(max_length=1)
	vendor = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	version = models.CharField(max_length=50, blank=True)
	cpe = models.CharField(max_length=255, unique=True)

	def __str__(self):
		return "%s %s %s" % (self.vendor, self.name, self.version)

	def get_full_name(self):
		return str(self)

class Vulnerability(models.Model):
	cve = models.CharField(max_length=50, unique=True)
	released_on = models.DateTimeField()
	modified_on = models.DateTimeField(blank=True, null=True)
	description = models.TextField()
	access_vector = models.CharField(max_length=20, default="NETWORK", null=True)
	access_complexity = models.CharField(max_length=20, default="MEDIUM", null=True)
	authentication = models.CharField(max_length=20, default="NONE", null=True)
	confidentiality_impact = models.CharField(max_length=20, default="NONE", null=True)
	integrity_impact = models.CharField(max_length=20, default="NONE", null=True)
	availability_impact = models.CharField(max_length=20, default="NONE", null=True)
	access_vector = models.CharField(max_length=20, default="NONE", null=True)
	product = models.ManyToManyField(Product)
	score = models.FloatField(default=0)

	def __str__(self):
		return self.cve

	def references(self):
		aux = []
		for row in VulnerabilitySource.objects.filter(vulnerability=self):
			aux.append(row.url)
		return aux

class VulnerabilitySource(models.Model):
	vulnerability = models.ForeignKey(Vulnerability)
	url = models.URLField(max_length=500)

import signals