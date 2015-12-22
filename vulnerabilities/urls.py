from rest_framework import routers
from django.conf.urls import url
from django.views.generic import TemplateView
from vulnerabilities.views import *

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'vulnerabilities', VulnerabilityViewSet, base_name='vulnerability')
urlpatterns = router.urls

urlpatterns += [
    url(r'^$', TemplateView.as_view(template_name="vulnerabilities/index.html")),
]