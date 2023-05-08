from django.db import models
from django.contrib.auth.models import User
import datetime
import pytz
utc=pytz.UTC

# Create your models here.
class VehicleModel(models.Model):
    make = models.CharField(verbose_name="Gamintojas", max_length=50)
    model = models.CharField(verbose_name="Modelis", max_length=50)


    def __str__(self):
        return f"{self.make} {self.model}"

    class Meta:          #Modeliu pavadinimai yra atvaizduojami teisingai vienaskaita ir daugiskaita (Autoservice skiltyje ir iejus i vidu)
        verbose_name = "Automobilio modelis"
        verbose_name_plural = "Automobilio modeliai"



class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=50)
    price = models.IntegerField(verbose_name="Kaina")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Paslauga"  #Modeliu pavadinimai yra atvaizduojami teisingai vienaskaita ir daugiskaita (Autoservice skiltyje ir iejus i vidu)
        verbose_name_plural = "Paslaugos"


class Vehicle(models.Model):
    plate = models.CharField(verbose_name="Valstybinis numeris", max_length=6)
    vin = models.CharField(verbose_name="VIN kodas", max_length=17)
    owner_name = models.CharField(verbose_name="Savininkas", max_length=50)
    vehicle_model = models.ForeignKey(to="VehicleModel", verbose_name="Automobilio modelis", on_delete=models.SET_NULL,
                                      null=True)
    photo = models.ImageField(verbose_name='Nuotrauka', upload_to="vehicles", null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle_model} ({self.plate})"

    class Meta:            #Modeliu pavadinimai yra atvaizduojami teisingai vienaskaita ir daugiskaita (Autoservice skiltyje ir iejus i vidu)
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

    LOAN_STATUS = (           #migracijas reikia pasidaryti nes kitaip klaida mes
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('a', 'Atsaukta'),
        ('t', 'Tvirtinama'),
        ('i', 'Ivykdita'),
    )

    status = models.CharField(verbose_name="Busena", max_length=1, choices=LOAN_STATUS, blank=True, default='t')

    class Meta:         #Modeliu pavadinimai yra atvaizduojami teisingai vienaskaita ir daugiskaita (Autoservice skiltyje ir iejus i vidu)
        verbose_name = "Uzsakymas"
        verbose_name_plural = "Uzsakymai"


class Order_line(models.Model):
    order = models.ForeignKey(to="Order", on_delete=models.CASCADE, related_name="lines")
    service = models.ForeignKey(to="Service", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(verbose_name="Kiekis")

    def sum(self):
        return self.service.price * self.quantity

    def __str__(self):
        return f"{self.order.vehicle} ({self.order.date}) : {self.service} - {self.quantity} "

    class Meta:
        verbose_name = "Uzsakymo eilute "   #Modeliu pavadinimai yra atvaizduojami teisingai vienaskaita ir daugiskaita (Autoservice skiltyje ir iejus i vidu)
        verbose_name_plural = "Uzsakymo eilutes"
