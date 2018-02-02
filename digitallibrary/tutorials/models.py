from __future__ import unicode_literals

from django.db import models

# Create your models here.
class SoftwareTutorials(models.Model):
    language = models.CharField(max_length=250)
    language_description = models.TextField()
    creator = models.CharField(max_length=250)
    lang_logo = models.FileField()
    
    def __str__(self):
        return self.language+' '+self.creator
    

class Book(models.Model):
    softwaretutorials = models.ForeignKey(SoftwareTutorials, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=250)
    book_author = models.CharField(max_length=250)
    pdf_file = models.FileField()
    price = models.IntegerField(default=0)
    
    def __str__(self):
        return self.book_title
    