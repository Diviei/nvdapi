from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from vulnerabilities.models import Vulnerability
from django.conf import settings
import twitter

api = twitter.Api(consumer_key = settings.TWITTER_CONSUMER_KEY,
                    consumer_secret = settings.TWITTER_CONSUMER_SECRET,
                    access_token_key = settings.TWITTER_ACCESS_TOKEN,
					access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET)

# method for updating vulnerability
@receiver(pre_save, sender=Vulnerability)
def vulnerability_updated(sender, instance, **kwargs):
	print "DEBUG"
	if instance.id:
		print "DEBUG2"
		aux = Vulnerability.objects.get(pk=instance.id)
		if instance.description != aux.description:
			print "DEBUG3"
			link = "https://web.nvd.nist.gov/view/vuln/detail?vulnId=%s" % instance.cve
			tweet = "UPDATED %s %s " % (instance.cve, link)
			#CELERY DELAY
			status = api.PostUpdate(tweet)
	else:
		print "NO ID"

# method for vulnerability created
@receiver(post_save, sender=Vulnerability)
def vulnerability_updated(sender, instance=None, created=False, **kwargs):
	if created:
		link = "https://web.nvd.nist.gov/view/vuln/detail?vulnId=%s" % instance.cve
		tweet = "NEW %s %s " % (instance.cve, link)
		#CELERY DELAY
		status = api.PostUpdate(tweet)