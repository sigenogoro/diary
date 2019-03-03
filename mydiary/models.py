from django.db import models
from django.utils import timezone
# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=100)
    hash_key = models.CharField(max_length=100,blank=True)
    content = models.TextField()
    related_hash = models.CharField(max_length=50, blank=True)
    day = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title + self.content + self.related_hash +  str(self.day)
