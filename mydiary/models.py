from django.db import models
from django.utils import timezone
# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    day = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title + ':' + self.content + str(self.day)