from django.contrib import admin
from vulnerabilities.models import *

admin.site.register(Vulnerability)
admin.site.register(Product)
admin.site.register(VulnerabilitySource)