from django import forms

class NewForm(forms.Form):
    input_text=forms.CharField(widget=forms.Textarea)

class Symptom_Addition(forms.Form):
    symptom=forms.CharField(label="Enter a new symptom:")
    specialist=forms.CharField(label="Enter the specialist:")
    weight=forms.FloatField(label="Enter the weight:")

class Disease_Addition(forms.Form):
    disease=forms.CharField(label="Enter a new disease: ")
    specialist=forms.CharField(label="Enter the specialist:")

class Dominant_Addition(forms.Form):
    keyword=forms.CharField(label="Enter a keyword: ")

class Symptom_Deletion(forms.Form):
    sym_dis=forms.CharField(label="Enter a symptom/disease to delete from the database:")

