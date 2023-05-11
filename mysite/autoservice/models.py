from django.db import models
from django.contrib.auth.models import User
import datetime
import pytz

utc = pytz.UTC
from tinymce.models import HTMLField
from PIL import Image


# Create your models here.
class VehicleModel(models.Model):
    make = models.CharField(verbose_name="Gamintojas", max_length=50)
    model = models.CharField(verbose_name="Modelis", max_length=50)

    def __str__(self):
        return f"{self.make} {self.model}"

    class Meta:  # Modeliu pavadinimai yra atvaizduojami teisingai vienaskaita ir daugiskaita (Autoservice skiltyje ir iejus i vidu)
        verbose_name = "Automobilio modelis"
        verbose_name_plural = "Automobilio modeliai"


class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=50)
    price = models.IntegerField(verbose_name="Kaina")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Paslauga"  # Modeliu pavadinimai yra atvaizduojami teisingai vienaskaita ir daugiskaita (Autoservice skiltyje ir iejus i vidu)
        verbose_name_plural = "Paslaugos"


class Vehicle(models.Model):
    plate = models.CharField(verbose_name="Valstybinis numeris", max_length=6)
    vin = models.CharField(verbose_name="VIN kodas", max_length=17)
    owner_name = models.CharField(verbose_name="Savininkas", max_length=50)
    vehicle_model = models.ForeignKey(to="VehicleModel", verbose_name="Automobilio modelis", on_delete=models.SET_NULL,
                                      null=True)
    photo = models.ImageField(verbose_name='Nuotrauka', upload_to="vehicles", null=True, blank=True)
    description = HTMLField(verbose_name="Aprasymas", null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle_model} ({self.plate})"

    class Meta:  # Modeliu pavadinimai yra atvaizduojami teisingai vienaskaita ir daugiskaita (Autoservice skiltyje ir iejus i vidu)
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"


class Order(models.Model):
    date = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    client = models.ForeignKey(to=User, verbose_name="Klientas", on_delete=models.SET_NULL, null=True, blank=True)
    vehicle = models.ForeignKey(to="Vehicle", verbose_name="Automobilis", on_delete=models.SET, null=True)
    deadline = models.DateTimeField(verbose_name="Terminas", null=True, blank=True)

    def deadline_overdue(self):
        return self.deadline and datetime.datetime.today().replace(tzinfo=utc) > self.deadline.replace(tzinfo=utc)

    def total(self):
        total_sum = 0
        for line in self.lines.all():
            total_sum += line.sum()
        return total_sum

    def __str__(self):
        return f"{self.vehicle} ({self.date})"

    LOAN_STATUS = (  # migracijas reikia pasidaryti nes kitaip klaida mes
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('a', 'Atsaukta'),
        ('t', 'Tvirtinama'),
        ('i', 'Ivykdita'),
    )

    status = models.CharField(verbose_name="Busena", max_length=1, choices=LOAN_STATUS, blank=True, default='t')


class Meta:  # Modeliu pavadinimai yra atvaizduojami teisingai vienaskaita ir daugiskaita (Autoservice skiltyje ir iejus i vidu)
    verbose_name = "Uzsakymas"
    verbose_name_plural = "Uzsakymai"
    ordering = ['-id']


class Order_line(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name="lines")
    service = models.ForeignKey(to="Service", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(verbose_name="Kiekis")

    def sum(self):
        return self.service.price * self.quantity

    def __str__(self):
        return f"{self.order.vehicle} ({self.order.date}) : {self.service} - {self.quantity} "

    class Meta:
        verbose_name = "Uzsakymo eilute "  # Modeliu pavadinimai yra atvaizduojami teisingai vienaskaita ir daugiskaita (Autoservice skiltyje ir iejus i vidu)
        verbose_name_plural = "Uzsakymo eilutes"


class OrderComment(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(to=User, verbose_name="Autorius", on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    content = models.TextField(verbose_name='Tekstas', max_length=5000)

    class Meta:
        verbose_name = "Komentaras"
        verbose_name_plural = 'Komentarai'
        ordering = ['-date_created']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
