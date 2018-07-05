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
    sentence="You have successfully updated disease."
    updation_disease(disease,specialist)
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
        data = pd.read_csv('example2.csv',header=None)
        data.columns=["Specialist","Symptom","Weight"]
        data_html = data.to_html()
        context = {'text': data_html}
        return render(request, "games/complete.html", context)
    
def view_disease(request):
    if request.method=="POST":
        data = pd.read_csv('DiseasesData.csv',header=None)
        data.columns=["Specialist","Disease"]
        data_html = data.to_html()
        context = {'text': data_html}
        return render(request, "games/complete.html", context)

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
    list1=[]
    with open('example2.csv') as fp:  
        line = fp.readline()
        while line:
            stripped_line=line.strip()
            stripped_line = stripped_line.lower()
            strip_list=stripped_line.split(",")
            list1.append(strip_list)
            line = fp.readline()
        fp.close()

    symptom=symptom.lower()
    specialist=specialist.lower()
    for element in list1:
        if element[0]==specialist and element[1]==symptom:
            return None
    fd=open('example2.csv','a',newline="")
    fd.write(specialist+","+ symptom+ "," +str(weight))
    fd.close()
    return None

def updation_disease(disease,specialist):
    list1=[]
    with open('DiseasesData.csv') as fp:  
        line = fp.readline()
        while line:
            stripped_line=line.strip()
            stripped_line = stripped_line.lower()
            strip_list=stripped_line.split(",")
            list1.append(strip_list)
            line = fp.readline()
        fp.close()

    disease=disease.lower()
    specialist=specialist.lower()
    for element in list1:
        if element[0]==specialist and element[1]==disease:
            return None
    fd=open('DiseasesData.csv','a',newline="")
    fd.write(specialist+","+ disease)
    fd.close()
    return None

def deletion(sym_dis):
    list1=[]
    with open('DiseasesData.csv') as fp:  
        line = fp.readline()
        while line:
            stripped_line=line.strip()
            stripped_line = stripped_line.lower()
            strip_list=stripped_line.split(",")
            list1.append(strip_list)
            line = fp.readline()
        fp.close()

    list2=[]
    sym_dis=sym_dis.lower()
    for element in list1:
        if element[1]!=sym_dis:
            list2.append(element)
    fd=open('DiseasesData.csv','w')
    fd.close()

    with open('DiseasesData.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        for i in list2:
            writer.writerow(i)

        csvfile.close()
    
    list1=[]
    with open('example2.csv') as fp:  
        line = fp.readline()
        while line:
            stripped_line=line.strip()
            stripped_line = stripped_line.lower()
            strip_list=stripped_line.split(",")
            list1.append(strip_list)
            line = fp.readline()
        fp.close()

    list2=[]
    for element in list1:
        if element[1]!=sym_dis:
            list2.append(element)
    fd=open('example2.csv','w')
    fd.close()

    with open('example2.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        for i in list2:
            writer.writerow(i)

        csvfile.close()
    
    return None

def updation_dominant(dominant,specialist):
    list1=[]
    with open('dominant.csv') as fp:  
        line = fp.readline()
        while line:
            stripped_line=line.strip()
            stripped_line = stripped_line.lower()
            strip_list=stripped_line.split(",")
            list1.append(strip_list)
            line = fp.readline()
        fp.close()

    dominant=dominant.lower()
    for element in list1:
        if element[0]==dominant:
            return None
    fd=open('dominant.csv','a',newline="")
    fd.write(dominant+","+specialist)
    fd.close()
    return None
