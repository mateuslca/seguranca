from django.db import models


class HoneypotLog(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	username = models.CharField(max_length=50)
	ipv4_address = models.CharField(max_length=15)
	ipv6_address = models.CharField(max_length=45)
	action = models.TextField()
	get_params = models.TextField()
	post_params = models.TextField()

	def __str__(self):
		return(f'{self.created_at} - {self.username} - {self.action}')
