from django.db import models
from django.utils import timezone
# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    next_action = models.TextField(blank=True)
    related_hash = models.CharField(max_length=50, blank=True)
    day = models.DateField(default=timezone.now)

    def __str__(self):
        return 'title：'+ self.title +'  '+ 'content：' + self.content + 'next_action：' + self.next_action + ' +  ' +'related_hash：' +  self.related_hash + '  ' +'day：' +  str(self.day)
