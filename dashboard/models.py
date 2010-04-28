from django.db import models

class MenuItem(models.Model):
	
	class Meta:
		verbose_name_plural = "Menu Items"
	
	
	name = models.CharField(max_length="200")
	url = models.CharField(max_length="1000", blank=True)
	toplevel = models.BooleanField(default=False)
	children = models.ManyToManyField('self', blank=True)
	
	def __unicode__(self):
		return self.name
