from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete

from django.dispatch import receiver

from django.core.validators import EmailValidator

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.IntegerField(blank=True)  
    message= models.TextField(max_length=20, blank=True)
    

    def __str__(self):
        return self.name + " - " + self.email




class Headline(models.Model):
  title = models.CharField(max_length=200)#title char(200)
  image = models.URLField(null=True, blank=True)#image
  url = models.TextField()
  average_rating = models.FloatField(default=0, null=True, blank=True)
  rating_count = models.IntegerField(default=0)
  def __str__(self):
    return f'{self.id} -> {self.title}'

  
class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.ForeignKey(Headline, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.headline.title}"


# stores all the rating given by all the users
class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.ForeignKey(Headline, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)

    def __str__(self):
        return f"{self.id} ->  ({self.user}) rated {self.headline.id} ({self.headline.title}) as {self.rating}"



# trigger if any rating is deleted(for eg, if any user gets deleted with respective ratings)
@receiver(post_delete, sender=Rating)
def recalculate_average_rating(sender, instance, **kwargs):
    # Calculate the new average rating for the deleted rating's headline
    ratings = Rating.objects.filter(headline=instance.headline)
    headline = instance.headline
    headline.rating_count = ratings.count()
    headline.average_rating = sum(r.rating for r in ratings) / headline.rating_count if headline.rating_count > 0 else 0
    headline.save()
