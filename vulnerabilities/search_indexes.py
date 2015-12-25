from haystack import indexes
from vulnerabilities.models import Vulnerability

class VulnerabilityIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    cve = indexes.CharField(model_attr='cve')
    modified_on = indexes.DateTimeField(model_attr='modified_on')

    def get_model(self):
        return Vulnerability

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()