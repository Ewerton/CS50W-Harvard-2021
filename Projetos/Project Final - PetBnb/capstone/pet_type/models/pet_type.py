from django.db import models


class PetType(models.Model):

    pet_type = models.CharField(max_length=70)

    @property
    def get_type(self):
        return self.pet_type

    class Meta:
        verbose_name = 'Pet Type'
        verbose_name_plural = 'Pet Types'
        ordering = ['id']
