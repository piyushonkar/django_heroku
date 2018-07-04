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
    return render(request,'games/complete.html',{'text':sentence})

    
#########################################################################

def add_disease(request):
    if request.method=="POST":
        my_form=Disease_Addition(request.POST)

        if my_form.is_valid():
            disease=my_form.cleaned_data['disease']
            specialist=my_form.cleaned_data['specialist']
    
    else:
        my_form=Disease_Addition()
    
    sentence="You have successfully updated disease."
    return render(request,'games/complete.html',{'text':sentence})

def add_dominant(request):
    if request.method=="POST":
        my_form=Dominant_Addition(request.POST)

        if my_form.is_valid():
            dominant=my_form.cleaned_data['keyword']
    
    else:
        my_form=Dominant_Addition()
    
    sentence="You have successfully updated dominant keywords."
    return render(request,'games/complete.html',{'text':sentence})

def view_symptom(request):
    if request.method=="POST":
        sentence="Here is the symptoms list"
        return render(request,'games/complete.html',{'text':sentence})
    
def view_disease(request):
    if request.method=="POST":
        sentence="Here is the disease list"
        return render(request,'games/complete.html',{'text':sentence})

def delete_symptom(request):
    if request.method=="POST":
        my_form=Symptom_Deletion(request.POST)

        if my_form.is_valid():
            dominant=my_form.cleaned_data['sym_dis']
    
    else:
        my_form=Symptom_Deletion()
    
    sentence="You have successfully deleted symptom"
    return render(request,'games/complete.html',{'text':sentence})
    
    
