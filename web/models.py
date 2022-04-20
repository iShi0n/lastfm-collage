from django.db import models


class Size(models.Model):
    size = models.CharField(max_length=5)
    items = models.IntegerField(default=25)
    collage_width = models.IntegerField(default=1000)
    collage_height = models.IntegerField(default=1000)
    art_width = models.IntegerField(default=200)
    art_height = models.IntegerField(default=200)

    def __str__(self) -> str:
        return self.size
