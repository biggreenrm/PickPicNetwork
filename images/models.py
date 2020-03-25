from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from autoslug import AutoSlugField


# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="images_created",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title')
    url = models.URLField()
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="images_liked", blank=True
    )

    # Определяет как будет отображаться модель в консоли
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            pass
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("images:detail", args=[self.id, self.slug])
