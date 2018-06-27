from .models import Album
from django.shortcuts import render,get_object_or_404
from .forms import NewForm
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
    