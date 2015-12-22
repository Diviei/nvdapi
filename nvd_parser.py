import re
import requests
from BeautifulSoup import BeautifulSoup as BS
import json
import datetime

class NVD_PARSER(object):
	"""
	Usage: 
	cveparsed = NVD_PARSER(cve="CVE-2014-0001")
	cveparsed.parse()
	"""
	def __init__(self, cve, html=None):
		self.cve = cve
		self.validCVE = False
		self.timeout = False
		self.url = "http://web.nvd.nist.gov/view/vuln/detail?vulnId=%s" % cve
		self.text = html
		self.release_date = ""
		self.description = ""
		self.cvss = ""

		self.references = []
		self.cpes = []

	def parse(self):
		if not self._get_html_code():
			return False
		else:
			self.validCVE = True

		try:
			self._parse_release_date()
			self._parse_description();
			self._parse_cvss()
			self.parse_impact()
			self._parse_references()
			self._parse_software()
			return True
		except Exception, e:
			self.validCVE = False
			print e
			return False

	def _get_html_code(self):
		print "Getting html code for %s..." % self.cve
		print "Url: %s" % self.url
		
		if not self.text:
			try:
				r = requests.get(self.url, timeout=5)
				self.text = r.text
			except Exception, e:
				self.timeout = True
				print e
				return False
		# #CVE Does not exists
		if "Unable to load vulnerability" in self.text:
			print "Unable to load vulnerability"
			return False

		if "DO NOT USE THIS CANDIDATE NUMBER" in self.text:
			print "CVE Rejected"
			return False

		return self.text

	def _parse_release_date(self):
		soup = BS(self.text)
		vulnDetail = soup.findAll('div', {'class':'vulnDetail'})[0]
		aux = re.findall(r'(\d{2}\/\d{2}\/\d{4})', str(vulnDetail))[0].split("/")
		self.release_date = datetime.date(int(aux[2]), int(aux[0]), int(aux[1]))

	def _parse_description(self):
		soup = BS(self.text)
		vulnDetail = soup.findAll('div', {'class':'vulnDetail'})[0]
		soup = BS(str(vulnDetail))
		rows = soup.findAll('p')
		self.description = str(rows[0]).replace("<p>","").replace("</p>","")

	def _parse_cvss(self):
		soup = BS(self.text)
		vulnDetail = soup.findAll('div', {'class':'vulnDetail'})[0]
		self.cvss = re.findall(r'(AV:\w\/AC:\w\/Au:\w\/C:\w\/I:\w\/A:\w)', str(vulnDetail))[0]

	def parse_impact(self):
		soup = BS(self.text)
		vulnDetail = soup.findAll('div', {'class':'vulnDetail'})[0]
		soup = BS(str(vulnDetail))
		rows = soup.findAll('div', {'class':'row'})
		if rows:
			for row in rows:
				if "Impact Type" in str(row):
					self.impact = str(row)
					self.impact = self.impact.replace('<div class="row">',"")
					self.impact = self.impact.replace('<span class="label">Impact Type:</span>',"")
					self.impact = self.impact.replace('</div>',"")
					self.impact = self.impact.lstrip().rstrip()
					break

	def _parse_references(self):
		print "Getting references..."
		soup = BS(self.text)
		vulnDetail = soup.findAll('div', {'id':'BodyPlaceHolder_cplPageContent_plcZones_lt_zoneCenter_VulnerabilityDetail_VulnFormView_VulnHyperlinksPanel'})[0]
		soup = BS(str(vulnDetail))
		rows = soup.findAll('a')
		for row in rows:
			if "nist.gov" not in str(row):
				self.references.append(row.get('href'))

	def _parse_software(self):
		print "Getting software..."
		soup = BS(self.text)
		vulnDetail = soup.findAll('div', {'id':'BodyPlaceHolder_cplPageContent_plcZones_lt_zoneCenter_VulnerabilityDetail_VulnFormView_VulnConfigurationsDiv'})[0]
		soup = BS(str(vulnDetail))
		rows = soup.findAll('a')
		for row in rows:
			if "nist.gov" not in row.next and "cpe" in row.next:
				self.cpes.append(row.next)
