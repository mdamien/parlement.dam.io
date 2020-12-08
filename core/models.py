from django.db import models

from nd15 import models as nd15_models


class Follow(models.Model):
    parlementaire_slug = models.CharField(max_length=255)
    email = models.EmailField()

    class Meta:
        unique_together = ['parlementaire_slug', 'email']