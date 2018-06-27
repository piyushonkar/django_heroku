from django import forms

class NewForm(forms.Form):
    input_text=forms.CharField(widget=forms.Textarea)