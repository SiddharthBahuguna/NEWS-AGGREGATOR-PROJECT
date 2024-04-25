from django.db import models

# Create your models here.

#create a user model by using Model class
#Headline will be the name of the table
#columns -> title,image,url
class Headline(models.Model):
  title = models.CharField(max_length=200)#title char(200)
  image = models.URLField(null=True, blank=True)#image
  url = models.TextField()
  def __str__(self):
    return self.title