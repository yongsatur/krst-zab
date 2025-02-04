from django.db import models
from django.contrib.auth.models import AbstractUser

class Regions(models.Model):
    nameRegion = models.CharField(verbose_name = 'Наименование района', max_length = 250, db_index = True)
    class Meta:
        ordering = ('nameRegion', )
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'

    def __str__(self):
        return self.nameRegion


class User(AbstractUser):
    region = models.ForeignKey(Regions, verbose_name=u"Район", blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        if self.region:
            return self.region.nameRegion
        else:
            return self.username
    