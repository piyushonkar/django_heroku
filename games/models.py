from django.db import models

# Create your models here.



class Chatbot(models.Model):
    word=models.CharField(max_length=200)
    specialist=models.CharField(max_length=200)
    type=models.CharField(max_length=200)
    weight=models.FloatField(default=0)

    def __str__(self):
        return self.word+"--"+self.specialist+"--"+self.type+"--"+str(self.weight)


