from django.db import models
from django.db.models.fields import CharField, DateTimeField, DateField
import datetime
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.



class Implant(models.Model):
    imp =[]
    sizes = ['4x5', '4x6', '5x5', '5x6', '6x5','6x6','3.5x8','3.5x10','3.5x11.5','3.5x13','3.5x15','4.3x8','4.3x10','4.3x11.5','4.3x13','4.3x15']
    types = ['Neodent Alvim CM', 'Neodent Drive CM',  'Neodent Titamax WS CM', 'Nobel Replace CM', 'SIN SWC CM', 'SIN Strong CM', 'SIN Unitite CM']
    SIZE_CHOICES = []
    TYPE_CHOICES = []
    

    for size in sizes:
        SIZE_CHOICES.append((str(size), str(size)))
    for type in types:
        TYPE_CHOICES.append((str(type), str(type)))

    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    size = models.CharField(max_length=30, choices=SIZE_CHOICES, default='3.5x8', unique=False)
    type = models.CharField(max_length=60, choices=TYPE_CHOICES, default='Neodent Alvim CM 3.5x8', unique=False)
    quantity = models.IntegerField(default=1, blank=False )

    def __str__(self):
        return  str(self.type + ' ' + self.size)

class Client(models.Model):
    gender_choices = [('Masculino', 'Masculino'),('Feminino', 'Feminino'), ('Outro', 'Outro')]

    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=80, null=False)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    obs = models.TextField(max_length=1000, blank=True)
    gender = models.CharField(max_length=50, blank=True, choices=gender_choices)

    def __str__(self):
        return str(self.full_name)

class Surgery(models.Model):
    imp =[]
    sizes = ['3.5x8','3.5x10','3.5x11.5','3.5x13','3.5x15','4.3x8','4.3x10','4.3x11.5','4.3x13','4.3x15']
    SIZE_CHOICES = []
    types = ['Neodent Alvim CM', 'Neodent Drive CM','Neodent Titamax WS CM', 'SIN SWC CM', 'SIN Strong CM', 'SIN Unitite CM']
    TYPE_CHOICES= []
    for type in types:
        TYPE_CHOICES.append((str(type), str(type)))

    for tipo in types:
        for size in sizes:
            impl = tipo + ' ' + size
            imp.append(impl)
    
    implantes = []
    for i in imp:
        impla = (str(i), str(i))
        implantes.append(impla)

    areaList = []
    ini = 11
    for i in range(11, 48):
        if i not in [19,20,29,30,39,40]:
            areaList.append((i, i))

    areas = map(tuple, areaList)
    for size in sizes:
        SIZE_CHOICES.append((str(size), str(size)))
    STAGE = {
        ('Espera', 'Espera'),
        ('Andamento', 'Andamento'), 
        ('Finalizado', 'Finalizado'), 
    }
    PMU = {
        ('Unitária', 'Unitária'),
        ('Múltipla', 'Múltipla'), 
        ('Protocolo', 'Protocolo'), 
    }
    today = datetime.date.today()
    date = today.strftime("%d/%m/%y")

    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    date = models.DateField( auto_now=False, default=date)
    quantity = models.PositiveIntegerField(default=0)
    implant_type = ArrayField(models.CharField(max_length=50, choices=TYPE_CHOICES))
    implant_size = ArrayField(models.CharField(max_length=50, choices=SIZE_CHOICES))
    area = ArrayField(models.CharField(max_length=50, choices=areaList))
    obs = models.TextField(blank=True, max_length=600)
    stage = models.CharField(max_length=50, choices=STAGE, default='Espera')
    pmu = models.CharField(max_length=20, choices=PMU, default='Unitária')

    def __str__(self):
        return str(self.client)



#
#prot = models.BooleanField(default=False)