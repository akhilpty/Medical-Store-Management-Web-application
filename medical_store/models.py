import datetime
from django.db import models



MED_TYPE=(
    ('liquid','LIQUID'),
    ('tablet','TABLET'),
    ('capsules','CAPSULES'),
    ('drops','DROPS'),
    ('injection','INJECTION'),
)

class Medicine(models.Model):
    medicine_name = models.CharField(max_length=200)
    medicine_type = models.CharField(max_length=20, choices=MED_TYPE, default='tablet')
    price = models.FloatField()
    count=models.IntegerField(null=True)
    medicine_arrived=models.DateField(default=datetime.date.today)
   
    medicine_company=models.CharField(max_length=50)

