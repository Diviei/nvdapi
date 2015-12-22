from rest_framework import serializers
from vulnerabilities.models import *

import time

class UnixEpochDateField(serializers.DateTimeField):
    def to_representation(self, value):
        """ Return epoch time for a datetime object or ``None``"""
        import time
        try:
            return int(time.mktime(value.timetuple()))
        except (AttributeError, TypeError):
            return None

    def to_internal_value(self, value):
        import datetime
        return datetime.datetime.fromtimestamp(int(value))

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product

class ProductVersionSerializer(serializers.ModelSerializer):
	vendor = serializers.CharField(source='product.vendor', read_only=True)
	name = serializers.CharField(source='product.name', read_only=True)
	class Meta:
		model = ProductVersion
		exclude = ('id','product')

class VulnerabilitySerializer(serializers.ModelSerializer):
	product_version = ProductVersionSerializer(many=True)
	references = serializers.StringRelatedField(many=True)
	released_on = UnixEpochDateField(read_only=True)
	modified_on = UnixEpochDateField(read_only=True)
	class Meta:
		model = Vulnerability
		exclude = ('id',)