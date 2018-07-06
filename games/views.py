from .models import *
from django.shortcuts import render,get_object_or_404
from .forms import *
from django.conf.urls import url
import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from autocorrect import spell
import numpy as np
from nltk.stem.lancaster import LancasterStemmer
from textblob import TextBlob
from .symptom_percent import *
import csv

###################################################################################


def start(request):
    form=NewForm()
    return render(request,"games/start.html",{'form':form})

def calculate(request):
    if request.method=="POST":
        my_form=NewForm(request.POST)

        if my_form.is_valid():
            text=my_form.cleaned_data['input_text']
    
    else:
        my_form=NewForm()
    
        
    sentence=computation(text)
    return render(request,'games/test.html',{'text':sentence})


#######################################################################

def add_deletion(request):
    form_symptom=Symptom_Addition()
    form_disease=Disease_Addition()
    form_dominant=Dominant_Addition()
    form_sym_del=Symptom_Deletion()
    context={
        'form_symptom':form_symptom,
        'form_disease':form_disease,
        'form_dominant':form_dominant,
        'form_sym_del':form_sym_del
    } 
    return render(request,'games/add_keyword.html',context)  

####################################################################

def add_symptom(request):
    if request.method=="POST":
        my_form=Symptom_Addition(request.POST)

        if my_form.is_valid():
            symptom=my_form.cleaned_data['symptom']
            specialist=my_form.cleaned_data['specialist']
            weight=my_form.cleaned_data['weight']
    
    else:
        my_form=Symptom_Addition()
    
    sentence="You have successfully updated symptoms."
    updation_symptom(symptom,specialist,weight)
    return render(request,'games/complete.html',{'text':sentence})

    
#########################################################################

def add_disease(request):
    if request.method=="POST":
        my_form=Disease_Addition(request.POST)

        if my_form.is_valid():
            specialist=my_form.cleaned_data['specialist']
            disease=my_form.cleaned_data['disease']
    
    else:
        my_form=Disease_Addition()
    updation_disease(disease,specialist)
    sentence="You have successfully added Disease."
    return render(request,'games/complete.html',{'text':sentence})

def add_dominant(request):
    if request.method=="POST":
        my_form=Dominant_Addition(request.POST)

        if my_form.is_valid():
            dominant=my_form.cleaned_data['keyword']
            specialist=my_form.cleaned_data['specialist']

    
    else:
        my_form=Dominant_Addition()
    sentence="You have successfully updated dominant keywords."
    updation_dominant(dominant,specialist)
    return render(request,'games/complete.html',{'text':sentence})

def view_symptom(request):
    if request.method=="POST":
        obj_symptoms=Symptom.objects.all()
        context = {'text': obj_symptoms}
        return render(request, "games/123.html", context)
    
def view_disease(request):
    if request.method=="POST":
        obj_diseases=Disease.objects.all()
        context = {'text': obj_diseases}
        return render(request, "games/123.html", context)

def delete_symptom(request):
    if request.method=="POST":
        my_form=Symptom_Deletion(request.POST)

        if my_form.is_valid():
            sym_dis=my_form.cleaned_data['sym_dis']
    
    else:
        my_form=Symptom_Deletion()
    
    sentence="You have successfully deleted symptom"
    deletion(sym_dis)
    return render(request,'games/complete.html',{'text':sentence})
    
    
def updation_symptom(symptom,specialist,weight):
    list1=Symptom.objects.all()

    symptom=symptom.lower()
    specialist=specialist.lower()
    for element in list1:
        if element.specialist.lower()==specialist and element.symptom.lower()==symptom:
            return None
    obj_symptom=Symptom()
    obj_symptom.specialist=specialist
    obj_symptom.symptom=symptom
    obj_symptom.weight=weight
    obj_symptom.save()
    return None

def updation_disease(disease,specialist):
    list1=Disease.objects.all()

    disease=disease.lower()
    specialist=specialist.lower()
    for element in list1:
        if element.specialist.lower()==specialist and element.disease.lower()==disease:
            return None
    obj_disease=Disease()
    obj_disease.specialist=specialist
    obj_disease.disease=disease
    obj_disease.save()
    return None

def deletion(sym_dis):
    list1=[]
    list1=Disease.objects.all()
    sym_dis = sym_dis.lower()
    for element in list1:
        if element.specialist.lower()==sym_dis:
            element.delete()
    
    list1=[]
    list1=Symptom.objects.all()
    for element in list1:
        if element.specialist.lower()==sym_dis:
            element.delete()
    
    return None


def updation_dominant(dominant,specialist):
    list1=[]
    list1=Keyword.objects.all()

    dominant=dominant.lower()
    specialist=specialist.lower()
    for element in list1:
        if element.specialist.lower()==specialist and element.keyword.lower()==dominant:
            return None
    obj_dominant=Keyword()
    obj_dominant.specialist=specialist
    obj_dominant.keyword=dominant
    obj_dominant.save()
    return None

