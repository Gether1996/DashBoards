from django.db.models import *
from django.utils.text import slugify
from django.urls import reverse

class Statistic(Model):
    name = CharField(max_length=200)
    slug = SlugField(blank=True)

    def get_absolute_url(self):
        return reverse("dashboard", kwargs={'slug': self.slug})

    @property
    def data(self):
        return self.dataitem_set.all()

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class DataItem(Model):
    statistic = ForeignKey(Statistic, on_delete=CASCADE)
    value = PositiveSmallIntegerField()
    owner = CharField(max_length=200)

    def __str__(self):
        return f"{self.owner}: {self.value}"