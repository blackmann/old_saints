from django.contrib.auth.models import User
from django.db import models


class House(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Alumnum(models.Model):
    user = models.OneToOneField(User, related_name="alumnum", on_delete=models.CASCADE)
    mobile = models.CharField(max_length=17)
    telephone = models.CharField(max_length=17, blank=True)
    whatsapp = models.CharField(max_length=17, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50)
    year_of_completion = models.IntegerField()
    exam_type = models.CharField(max_length=20) # o/a level, sss, wassce
    house = models.ForeignKey(House, related_name="alumni", on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, related_name="alumni", on_delete=models.CASCADE)
    member_id = models.CharField(max_length=20)
    profession = models.CharField(max_length=100)

    reference_1 = models.TextField(blank=True)
    reference_2 = models.TextField(blank=True)
    
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()


class Dues(models.Model):
    alumnum = models.ForeignKey(Alumnum, related_name="dues", on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now=True)

