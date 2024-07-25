from django.db import models
from django.contrib.auth.models import User
STATE_CHOICES=(
('Andhra Pradesh','Andhra Pradesh'),
('Arunachal Pradesh','Arunachal Pradesh'),
('Assam','Assam'),
('Bihar','Bihar'),
('Chandigarh','Chandigarh'),
('Chhattisgarh','Chhattisgarh'),
('Delhi','Delhi'),
('Goa','Goa'),
('Gujarat','Gujarat'),
('Haryana','Haryana'),
('Himachal Pradesh','Himachal Pradesh'),
('Jammu & Kashmir','Jammu & Kashmir'),
('Jharkhand','Jharkhand'),
('Karnataka','Karnataka'),
('Kerala','Kerala'),
('Madhya Pradesh','Madhya Pradesh'),
('Maharashtra','Maharashtra'),
('Manipur','Manipur'),
('Meghalaya','Meghalaya'),
('Mizoram','Mizoram'),
('Nagaland','Nagaland'),
('Odisha','Odisha'),
('Puducherry','Puducherry'),
('Punjab','Punjab'),
('Rajasthan','Rajasthan'),
('Sikkim','Sikkim'),
('Tamil Nadu','Tamil Nadu'),
('Telangana','Telangana'),
('Tripura','Tripura'),
('Uttar Pradesh','Uttar Pradesh'),
('Uttarakhand','Uttarakhand'),
('West Bengal','West Bengal')
)


class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=100)
    
    def __str__(self) -> str:
        return self.name 
    
CATEGORY_CHOICES=(
    ('Cough','Cough'),
    ('Fever','Fever'),
    ('SkinCare','Skin Care'),
    ('FitnessandWellness','Fitness and Wellness'),
    ('BabyCare','Baby Care'),
    ('Diabetis','Diabetis'),
)

class Medicine(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=30)
    disease=models.CharField(choices=CATEGORY_CHOICES,max_length=30)
    description=models.CharField(max_length=1000)
    dosage=models.CharField(max_length=500)
    price=models.CharField(max_length=500,default='Rs. 200')
    image=models.URLField()


    def __str__(self) -> str:
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    medicine=models.ForeignKey(Medicine,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * 200


