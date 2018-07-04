from django.db import models

# Create your models here.

class Symptom(models.Model):
    symptom=models.CharField(max_length=100)
    specialist=models.CharField(max_length=100)
    weight=models.FloatField(max_length=100)

    def __str__(self):
        return self.symptom +"-"+ self.specialist + "-" + self.weight


class Disease(models.Model):
    disease=models.CharField(max_length=100)
    specialist=models.CharField(max_length=100)

    def __str__(self):
        return self.disease + "-" + self.specialist


class Keyword(models.Model):
    keyword=models.CharField(max_length=100)
    specialist=models.CharField(max_length=100)

    def __str__(self):
        return self.keyword + "-" + self.specialist 

