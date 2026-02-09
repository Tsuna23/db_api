from django.db import models
from django.utils.translation import gettext_lazy as _
class CategoryChoices(models.TextChoices):
    ALIMENTAIRE = 'alimentaire', _('Alimentaire')
    ANIMAL = 'animal', _('Animal')
    EQUIPEMENT = 'equipement', _('Équipements')

class Product(models.Model):
    category = models.CharField(
        max_length=20,
        choices=CategoryChoices.choices,
        verbose_name="Catégorie"
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name="Image",
        null=True,
        blank=True
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Titre"
    )
    desc = models.TextField(
        verbose_name="Description"
    )
    price = models.CharField(
        max_length=50,
        verbose_name="Prix"
    )

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return f"{self.title} - {self.price}"
