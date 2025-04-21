from django.db import models


class HoneypotLog(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	username = models.CharField(max_length=255, null=True, blank=True)
	ipv4_address = models.GenericIPAddressField()
	post_params = models.JSONField(default=dict)

	def __str__(self):
		return(f'[{self.timestamp}] - {self.username} - {self.ipv4_address}')
