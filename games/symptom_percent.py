# DOCUMENTATION:
'''
The funtions declared are as follows:
	correction(sentence,List) :- returns a string of corrected words after removing stopwords and implementing autocorrect.

The variables and their datatypes and structures are as follows:
	stop_words: 		a SET of stopwords in english.
	sentence: 			a STRING that the user inputs (query).
	word_tokens: 		a LIST of words that the user enters.
	symptom_list: 		LIST of symptoms as read from the csv file.
	disease_list: 		LIST of diseases as read from the csv file.
	psych_list: 		LIST of diseases that are only treated by a psychiatrist, this will be checked only if none of the other cases match.
	keyword_list: 		LIST containing the words of all the above 3 lists. If the user entered words match any of the keywords then it will not be autocorrected.
	male: 				LIST of all the words pointing to male user.
	female: 			LIST of all the words pointing to female user.
	symptom_dict: 		DICTIONARY containing the matched list of specialists and their total weights/values.
	dominany_key: 		empty STRING that will contain the name of specialist if any dominant keyword is present.
	psych_present: 		empty STRING that will contain psychiatrist if the co-dominant keywords match.
	primary: 			LIST containing the dominant keywords
	primary_indices: 	DICTIONARY containing dominant keywords found in the list as keys and their indexes in the sentence as values.
	disease: 			empty STRING which will store the disease if found in the sentence.
	specialist:	 		empty STRING which will store the corresponding specialist of the disease found in the sentence.
	flag: 				0 if no disease found, 1 if a disease is found.
	min_key: 			minimum indexed dominant keyword.
	value: 				INT or FLOAT variable storing total weight of a particular specialist based on the number of symptoms pertaining to that specialist. 
	new_list: 			LIST containing the dictionary values as elements of the list in descending order of weights.
	print_list: 		subLIST of the new_list containing only the first two elements.

The packages imported are as follows:
	nltk version 3.3
	pandas version 0.23.0
	autocorrect version 0.3.0
'''

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from autocorrect import spell
from textblob import TextBlob
from .models import *

#################################################################

# To filter the unwanted words in the sentence and also apply autocorrect
def correction(sentence,List):
	stop_words=set(stopwords.words('english'))
	word_tokens = word_tokenize(sentence)
	stop_words.remove('a')
	stop_words.remove('and')
	stop_words.remove('are')
	stop_words.remove('the')
	stop_words.remove('to')
	stop_words.remove('in')
	stop_words.remove('of')
	stop_words.remove('on')
	stop_words.remove('for')
	stop_words.remove('at')
	stop_words.remove('from')
	stop_words.remove('up')
	print("\n")
	words=[]
	filtered_sentence = [w for w in word_tokens if not w in stop_words]
	symbols=["," , ":" , ".","-"]
	sent=[w for w in filtered_sentence if not w in symbols]
	for w in sent:
	 	if w in List:
	 		words.append(w)
	 	else:
	 		try:
	 			words.append(str(float(w)))
	 		except:
	 			m=spell(w)
	 			words.append(m.lower())
	x=" ".join(words)
	return(x)

########################################################################################################
def computation(sentence):
	# To read the files and append the keywords, diseases and symptoms in the respective lists
	sentence=sentence.lower()
	symptom_list=[]
	keyword_list=[]
	disease_list=[]
	psych_list=[]
	short_disease_list=[]

	####################################################################################################################

	# To detect the input language and translate it to english if it's not in english
	text_input=TextBlob(sentence)
	lang=text_input.detect_language()
	if lang!='en':
		sentence=text_input.translate(to='en')
	sentence=str(sentence)

	############################################################################################################
	
	obj_symptom=Chatbot.objects.filter(type__startswith='sym')
	for element in obj_symptom:
		specialist=element.specialist.lower()
		symptom=element.word.lower()
		keyword_list.append(specialist)
		keyword_list.append(symptom)
		weight=element.weight
		symptom_list.append([specialist,symptom,weight])

	obj_disease=Chatbot.objects.filter(type__startswith='dis')
	for element in obj_disease:
		specialist=element.specialist.lower()
		disease=element.word.lower()
		keyword_list.append(disease)
		keyword_list.append(specialist)
		disease_list.append([specialist,disease])

	psych_list=[['psychiatrist', 'abnormal behavior', '3'], ['psychiatrist', 'adhd child', '4'], ['psychiatrist', 'adjustment problem', '5'], ['psychiatrist', 'aggressive', '4'], ['psychiatrist', 'angel tour', '3.5'], ['psychiatrist', 'anxiety', '3'], ['psychiatrist', 'big talks', '1.5'], ['psychiatrist', 'confusion', '1'], ['psychiatrist', 'craving', '4'], ['psychiatrist', 'craving for food','2.5'], ['psychiatrist', 'crawling sensation', '4'], ['psychiatrist', 'cry', '4.5'], ['psychiatrist', 'decrease in social skills', '2.5'], ['psychiatrist', 'delay in learning language skills', '3.5'], ['psychiatrist', 'depressed mood', '3'], ['psychiatrist', 'depression', '5'], ['psychiatrist', 'desire for food', '5'], ['psychiatrist', 'difficult to pay attention', '2.5'], ['psychiatrist', 'difficult to wake up from sleep', '5'], ['psychiatrist', 'difficulty in finding word', '5'], ['psychiatrist', 'difficulty in sleep', '4'], ['psychiatrist', 'disorder', '5'], ['psychiatrist', 'dizziness', '2'], ['psychiatrist', 'dizzy', '3'], ['psychiatrist', 'emotions', '3'], ['psychiatrist', 'fatigue', '3'], ['psychiatrist', 'fear', '1'], ['psychiatrist', 'fear of water', '1.5'], ['psychiatrist', 'fear of wind', '4.5'], ['psychiatrist', 'feeling of pressure or heaviness', '4.5'], ['psychiatrist', 'feeling walking on some skull', '5'], ['psychiatrist', 'fluctuations of mood', '1'], ['psychiatrist', 'frightening dreams', '4'], ['psychiatrist', 'frightening thoughts', '5'], ['psychiatrist', 'hallucination', '4.5'], ['psychiatrist', 'hyperactive', '5'], ['psychiatrist', 'hypertension', '4'], ['psychiatrist', 'inappropriate behavior', '4'], ['psychiatrist', 'intense desire for food', '4'], ['psychiatrist', 'lack of happiness', '1'],['psychiatrist', 'lack of self care', '5'], ['psychiatrist', 'lack of sense', '4.5'], ['psychiatrist', 'lack of sleep', '3.5'], ['psychiatrist', 'lack of social skills', '5'], ['psychiatrist', 'memory problem', '3.5'], ['psychiatrist', 'memory related problem', '4'], ['psychiatrist', 'mentally retarded ', '4'], ['psychiatrist', 'numb head', '5'], ['psychiatrist', 'numbness of head', '2'], ['psychiatrist', 'personality change', '2'], ['psychiatrist', 'perspiration', '5'], ['psychiatrist', 'phobia', '3.5'], ['psychiatrist', 'problem in learning language skills', '2.5'], ['psychiatrist', 'problem in waking up from sleep', '4'], ['psychiatrist', 'repeated thoughts of checking', '5'], ['psychiatrist', 'repeating same thing', '5'], ['psychiatrist', 'repeatingthe phrases', '4'], ['psychiatrist', 'repeating the words', '4'], ['psychiatrist', 'restless', '4'], ['psychiatrist', 'revolving sensation', '4'], ['psychiatrist', 'sadness', '3'], ['psychiatrist', 'scary dreams', '3.5'], ['psychiatrist', 'scary thoughts', '5'], ['psychiatrist', 'shak', '4.5'], ['psychiatrist', 'sleep disturbance', '3.5'], ['psychiatrist', 'spitting', '3.5'], ['psychiatrist', 'stress', '1'], ['psychiatrist', 'to cry', '4.5'], ['psychiatrist', 'unconscious', '3.5'], ['psychiatrist', 'unconsciousness', '1.5'], ['psychiatrist', 'unrest', '1.5'], ['psychiatrist', 'violent', '2.5'], ['psychiatrist', 'waham', '3.5'], ['psychiatrist', 'wander', '4']]
	for qaz in psych_list:
		keyword_list.append(qaz[0])
		a=qaz[1].split(" ")
		keyword_list.extend(a)

	short_disease_list=[['gastroenterologist', 'gerd'], ['gastroenterologist', 'ibl'], ['gastroenterologist', 'sod'], ['neurologist', 'als'], ['oncologist', 'aml'], ['oncologist', 'cll'], ['oncologist', 'cml'], ['oncologist', 'gist'], ['oncologist', 'mds'], ['psychiatrist', 'adhd'], ['psychiatrist', 'ocd'], ['psychiatrist', 'ptsd'], ['pulmonologist', 'ards'], ['pulmonologist', 'copd'], ['pulmonologist','ild'], ['pulmonologist', 'tb'], ['sexologist', 'hiv'], ['sexologist', 'std'], ['urologist', 'ed'], ['hematologist', 'itp'], ['gynecologist', 'pcod'], ['gynecologist', 'pcos']]
	for qaz in short_disease_list:
		keyword_list.append(qaz[0])
		keyword_list.append(qaz[0])


	keyword_list=list(set(keyword_list))	
	sentence=correction(sentence,keyword_list)


	###############################################################################################

	# To read the file and append the male and female words in their lists accordingly
	male=['boy', 'nephew', 'guy', 'male', 'husband', 'brother', 'he', 'son', 'papa', 'grandfather', 'grandad', 'father', 'uncle', 'uncle', 'Mr.', 'Mr.', 'gent', 'lad', 'master', 'sir', 'sir', 'bro', 'boyfriend']
	female=['girl', 'niece', 'gal', 'female', 'wife', 'sister', 'she', 'daughter', 'maa', 'grandmother', 'grandmom', 'mother', 'aunt', 'aunty', 'Mrs.', 'Miss.', 'lady', 'lass', 'miss', "ma'am", 'madam', 'sis', 'girlfriend']
	gender=''
	for sex in word_tokenize(sentence):
		if sex in male:
			gender='Male'
			break
		elif sex in female:
			gender='Female'
			break

	#####################################################################################

	# Step1: check if any disease is mentioned, if yes, send it to the specialist. If not, move to step 2
	# Step2: check if anydominant keyword is present, if yes, send it to the specialist. If not, move to step 3
	# Step3: check if symptoms match those in the symptom_list, if yes, calculate accordingly. If not, move to step 4
	# Step4: check if any psychiatric symptoms are present, if yes, refer to a psychiatrist. End.
	symptom_dict={}
	dominant_key=''
	psych_present=''
	primary=['sex', 'cancer','abortion','penis','testes','testicles']
	primary_indices={}
	flag=0
	disease=""
	specialist=""
	flag_short=0

	#####################################################################

	for element in short_disease_list:
		for item in word_tokenize(sentence):
			if item==element[1]:
				disease=element[1]
				specialist=element[0]
				flag_short=1
				break
				
	######################################################################
	if flag_short==1:
		if lang=='en':
			return('You should consult a ' + specialist)
		else:
			output_text=TextBlob("You should consult a " + specialist)
			output_text=output_text.translate(to=lang)
			return(output_text)

	else:
		for element in disease_list:
			if sentence.find(element[1])>=0:
				flag=1
				disease=element[1]
				specialist=element[0]
				break
		if flag==1:
			if lang=='en':
				return("You should consult a " + specialist)
			else:
				output_text=TextBlob("You should consult a " + specialist)
				output_text=output_text.translate(to=lang)
				return(output_text)
			quit()

		elif flag==0:	
			for m in primary:
				if sentence.find(m)>=0:
					primary_indices[m]=sentence.find(m)

			min_key=''

			for key,value in primary_indices.items():
				if primary_indices[key]==min(primary_indices.values()):
					min_key=key

			if min_key=='sex':
				if gender=='Female' or sentence.find('pregnancy')>=0 or sentence.find('pregnant')>=0 or sentence.find('period')>=0 :
					if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
						dominant_key='gynaecologist'
						psych_present='psychiatrist'
						if lang=='en':
							return('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
						else:
							output_text=TextBlob('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
							output_text=output_text.translate(to=lang)
							return(output_text)
						quit()
					else:
						dominant_key='gynaecologist'
						if lang=='en':
							return('There is a high probability that you should consult a '+dominant_key)
						else:
							output_text=TextBlob('There is a high probability that you should consult a '+dominant_key)
							output_text=output_text.translate(to=lang)
							return(output_text)
						quit()
				else:
					if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
						dominant_key='sexologist'
						psych_present='psychiatrist'
						if lang=='en':
							return('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
						else:
							output_text=TextBlob('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
							output_text=output_text.translate(to=lang)
							return(output_text)
							quit()
					elif sentence.find('period')>=0 or sentence.find('abortion')>=0:
						dominant_key='gynaecologist'
						if lang=='en':
							return('There is a high probability that you should consult a '+dominant_key)
						else:
							output_text=TextBlob('There is a high probability that you should consult a '+dominant_key)
							output_text=output_text.translate(to=lang)
							return(output_text)
							quit()
					else:
						dominant_key='sexologist'
						if lang=='en':
							return('There is a high probability that you should consult a '+dominant_key)
						else:
							output_text=TextBlob('There is a high probability that you should consult a '+dominant_key)
							output_text=output_text.translate(to=lang)
							return(output_text)
						quit()

			elif min_key=='penis':
				if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
					dominant_key='sexologist'
					psych_present='psychiatrist'
					if lang=='en':
						return('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
					else:
						output_text=TextBlob('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
						output_text=output_text.translate(to=lang)
						return(output_text)	
				else:
					dominant_key='sexologist'
					if lang=='en':
						return('There is a high probability that you should consult a '+dominant_key)
					else:
						output_text=TextBlob('There is a high probability that you should consult a '+dominant_key)
						output_text=output_text.translate(to=lang)
						return(output_text)
				quit()

			elif min_key=='testicles':
				if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
					dominant_key='sexologist'
					psych_present='psychiatrist'
					if lang=='en':
						return('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
					else :
						output_text=TextBlob('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
						output_text=output_text.translate(to=lang)
						return(output_text)
				else:
					dominant_key='sexologist'
					if lang=='en':
						return('There is a high probability that you should consult a '+dominant_key)
					else:
						output_text=TextBlob('There is a high probability that you should consult a '+dominant_key)
						output_text=output_text.translate(to=lang)
						return(output_text)
				quit()
						
			elif min_key=='testes':
				if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
					dominant_key='sexologist'
					psych_present='psychiatrist'
					if lang=='en':
						return('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
					else:
						output_text=TextBlob('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
						output_text=output_text.translate(to=lang)
						return(output_text)		
				else:
					dominant_key='sexologist'
					if lang=='en':
						return('There is a high probability that you should consult a '+dominant_key)
					else:
						output_text=TextBlob('There is a high probability that you should consult a '+dominant_key)
						output_text=output_text.translate(to=lang)
						return(output_text)
				quit()								
				
			elif min_key=='cancer':
				dominant_key='oncologist'
				if lang=='en':
					return('There is a high probability that you should consult a '+ dominant_key)
				else:
					output_text=TextBlob('There is a high probability that you should consult a '+ dominant_key)
					output_text=output_text.translate(to=lang)
					return(output_text)
				quit()

			elif sentence.find('abortion')>=0 or sentence.find('period')>=0 :
				if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
					dominant_key='gynaecologist'
					psych_present='psychiatrist'
					if lang=='en':
						return('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
					else:
						output_text=TextBlob('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
						output_text=output_text.translate(to=lang)
						return(output_text)
				else:
					dominant_key='gynaecologist'
					if lang=='en':
						return('There is a high probability that you should consult a '+dominant_key)
					else:
						output_text=TextBlob('There is a high probability that you should consult a '+dominant_key)
						output_text=output_text.translate(to=lang)
						return(output_text)
				quit()
			
			else:
				for element in symptom_list:
					if sentence.find(element[1]) >= 0 :
						if not (element[0] in symptom_dict.keys()):
							symptom_dict[element[0]]=float(element[2])
						else:
							value=symptom_dict[element[0]]+float(element[2])
							symptom_dict[element[0]]=value
				total=0
				for value in symptom_dict.values():
					total = total + value
				for key in symptom_dict.keys():
					symptom_dict[key] = symptom_dict[key]*100/total

				new_list=sorted(symptom_dict.items(), key = lambda t: t[1], reverse = True)
				print_list=[]
				flag1=0
				for item in new_list:
					flag1=flag1+1
					if flag1 < 3:
						print_list.append(item[0])
				if print_list!=[]:
					if lang=='en':
						return('Based on the analysis you should consult a '+' and '.join(print_list))
					else:
						output_text=TextBlob('Based on the symptoms you should consult a '+' and '.join(print_list))
						output_text=output_text.translate(to=lang)
						return(output_text)
					quit()
				if symptom_dict=={}:
					for element in psych_list:
						if sentence.find(element[1])>=0:
							if lang=='en':
								return('You should visit a psychiatrist')
							else:
								output_text=TextBlob('You should visit a psychiatrist')
								output_text=output_text.translate(to=lang)
								return(output_text)
							quit()