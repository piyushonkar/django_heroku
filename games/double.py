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
import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from autocorrect import spell
import json
import unicodedata
import random
import tflearn
import tensorflow as tf
import numpy as np
from nltk.stem.lancaster import LancasterStemmer
from textblob import TextBlob

#################################################################

# method to remove punctuations from sentences.
def remove_punctuation(text):
    return text.translate(tbl)

# a method that takes in a sentence and list of all words
# and returns the data in a form the can be fed to tensorflow
def get_tf_record(sentence):
    global words1
    # tokenize the pattern
    sentence_words = word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    # bag of words
    bow = [0]*len(words1)
    for s in sentence_words:
        for i,w in enumerate(words1):
            if w == s:
                bow[i] = 1
    return(np.array(bow))
                
#####################################################################

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
if __name__=="__main__":
    file_name=sys.argv[1]
    file_temp= open(file_name,'w')
    # To read the files and append the keywords, diseases and symptoms in the respective lists
    sentence=" ".join(sys.argv[2:])
    sentence=sentence.lower()
    filepath = 'example2.csv'
    symptom_list=[]
    keyword_list=[]
    disease_list=[]
    psych_list=[]
    short_disease_list=[]

    ####################################################################################

    # To detect the input language and translate it to english if it's not in english
    text_input=TextBlob(sentence)
    lang=text_input.detect_language()
    if lang!='en':
        sentence=text_input.translate(to='en')
    sentence=str(sentence)

    ###################################################################################


    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            stripped_line=line.strip()
            stripped_line = stripped_line.lower()
            strip_list=stripped_line.split(",")
            a=strip_list[0].split(" ")
            b=strip_list[1].split(" ")
            keyword_list.extend(a)
            keyword_list.extend(b)
            symptom_list.append(strip_list)
            line = fp.readline()

    with open('DiseasesData.csv') as fp:
        line = fp.readline()
        while line:
            stripped_line=line.strip()
            stripped_line=stripped_line.lower()
            strip_list=stripped_line.split(",")
            a=strip_list[0].split(" ")
            b=strip_list[1].split(" ")
            keyword_list.extend(a)
            keyword_list.extend(b)
            disease_list.append(strip_list)
            line=fp.readline()

    with open('psychiatrist.csv') as fp:
        line = fp.readline()
        while line:
            stripped_line=line.strip()
            stripped_line=stripped_line.lower()
            strip_list=stripped_line.split(",")
            a=strip_list[0].split(" ")
            b=strip_list[1].split(" ")
            keyword_list.extend(a)
            keyword_list.extend(b)
            psych_list.append(strip_list)
            line=fp.readline()

    with open('short_diseases.csv') as fp:
        line = fp.readline()
        while line:
            stripped_line=line.strip()
            stripped_line=stripped_line.lower()
            strip_list=stripped_line.split(",")
            a=strip_list[0].split(" ")
            b=strip_list[1].split(" ")
            keyword_list.extend(a)
            keyword_list.extend(b)
            short_disease_list.append(strip_list)
            line=fp.readline()

    keyword_list=list(set(keyword_list))	
    sentence=correction(sentence,keyword_list)


    ###############################################################################################

    # To read the file and append the male and female words in their lists accordingly
    male=[]
    female=[]
    filename='MaleFemale.csv'
    dataset=pd.read_csv(filename)
    array=dataset.values
    for i in array:
        male.append(i[0])
        female.append(i[1])

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
    # Step2: check if any dominant keyword is present, if yes, send it to the specialist. If not, move to step 3
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
    for elements in short_disease_list:
        if elements[1] in word_tokenize(sentence):
            specialist1=elements[0]
            file_temp.write('In our opinion you should consult a '+specialist1)
            break
        else:
            for element in disease_list:
                if sentence.find(element[1])>=0:
                    flag=1
                    disease=element[1]
                    specialist=element[0]
                    break
            if flag==1:
                if lang=='en':
                    file_temp.write("You should consult a" + specialist + "for"+ disease)
                else:
                    output_text=TextBlob("You should consult a" + specialist + "for"+ disease)
                    output_text=output_text.translate(to=lang)
                    file_temp.write(output_text)
                break
            elif flag==0:
                for m in primary:
                    if sentence.find(m)>=0:
                        primary_indices[m]=sentence.find(m)
                min_key=''
                for key,value in primary_indices.items():
                    if primary_indices[key]==min(primary_indices.values()):
                        min_key=key
                if min_key=='sex':
                    if gender=='Female' or sentence.find('pregnancy')>=0 or sentence.find('pregnant')>=0 or sentence.find('period')>=0:
                        if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0:
                            dominant_key='gynaecologist'
                            psych_present='psychiatrist'
                            if lang=='en':
                                file_temp.write('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
                            else:
                                output_text=TextBlob('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
                                output_text=output_text.translate(to=lang)
                                file_temp.write(output_text)
                            break
                        else:
                            dominant_key='gynaecologist'
                            if lang=='en':
                                file_temp.write('There is a high probability that you should consult a '+dominant_key)
                            else:
                                output_text=TextBlob('There is a high probability that you should consult a '+dominant_key)
                                output_text=output_text.translate(to=lang)
                                file_temp.write(output_text)
                            break
                    else:
                        if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
                            dominant_key='sexologist'
                            psych_present='psychiatrist'
                            if lang=='en':
                                file_temp.write('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
                            else:
                                output_text=TextBlob('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
                                output_text=output_text.translate(to=lang)
                                file_temp.write(output_text)
                                break
                        elif sentence.find('period')>=0 or sentence.find('abortion')>=0:
                            dominant_key='gynaecologist'
                            if lang=='en':
                                file_temp.write('There is a high probability that you should consult a '+dominant_key)
                            else:
                                output_text=TextBlob('There is a high probability that you should consult a '+dominant_key)
                                output_text=output_text.translate(to=lang)
                                file_temp.write(output_text)
                                break
                        else:
                            dominant_key='sexologist'
                            if lang=='en':
                                file_temp.write('There is a high probability that you should consult a '+dominant_key)
                            else:
                                output_text=TextBlob('There is a high probability that you should consult a '+dominant_key)
                                output_text=output_text.translate(to=lang)
                                file_temp.write(output_text)
                            break
                elif min_key=='penis':
                    if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
                        dominant_key='sexologist'
                        psych_present='psychiatrist'
                        if lang=='en':
                            file_temp.write('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
                        else:
                            output_text=TextBlob('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
                            output_text=output_text.translate(to=lang)
                            file_temp.write(output_text)							
                        break
                elif min_key=='testicles':
                    if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
                        dominant_key='sexologist'
                        psych_present='psychiatrist'
                        if lang=='en':
                            file_temp.write('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
                        else :
                            output_text=TextBlob('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
                            output_text=output_text.translate(to=lang)
                            file_temp.write(output_text)
                        break
                elif min_key=='testes':
                    if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
                        dominant_key='sexologist'
                        psych_present='psychiatrist'
                        if lang=='en':
                            file_temp.write('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
                        else:
                            output_text=TextBlob('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
                            output_text=output_text.translate(to=lang)
                            file_temp.write(output_text)						
                        break
                elif min_key=='cancer':
                    dominant_key='oncologist'
                    if lang=='en':
                        file_temp.write('There is a high probability that you should consult a '+ dominant_key)
                    else:
                        output_text=TextBlob('There is a high probability that you should consult a '+ dominant_key)
                        output_text=output_text.translate(to=lang)
                        file_temp.write(output_text)
                    break
                elif sentence.find('abortion')>=0 or sentence.find('period')>=0 :
                    if sentence.find('hypertension')>=0 or sentence.find('anxiety')>=0 or sentence.find('stress')>=0 or sentence.find('depression')>=0 :
                        dominant_key='gynaecologist'
                        psych_present='psychiatrist'
                        if lang=='en':
                            file_temp.write('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
                        else:
                            output_text=TextBlob('There is a high probability that you should consult a '+dominant_key+' and '+psych_present)
                            output_text=output_text.translate(to=lang)
                            file_temp.write(output_text)
                        break
                    else:
                        dominant_key='gynaecologist'
                        if lang=='en':
                            file_temp.write('There is a high probability that you should consult a '+dominant_key)
                        else:
                            output_text=TextBlob('There is a high probability that you should consult a '+dominant_key)
                            output_text=output_text.translate(to=lang)
                            file_temp.write(output_text)
                        break
                else:
                    # a table structure to hold the different punctuation used
                    tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                                                        if unicodedata.category(chr(i)).startswith('P'))
                    #initialize the stemmer
                    stemmer = LancasterStemmer()
                    #variable to hold the Json data read from the file
                    data = None
                    # read the json file and load the training data
                    with open('tensorjson.json') as json_data:
                        data = json.load(json_data)
                    # get a list of all categories to train for
                    categories = list(data.keys())
                    words1 = []
                    # a list of tuples with words in the sentence and category name 
                    docs = []
                    for each_category in data.keys():
                        for each_sentence in data[each_category]: 
                            # remove any punctuation from the sentence
                            each_sentence = remove_punctuation(each_sentence)
                            # extract words from each sentence and append to the word list
                            w = word_tokenize(each_sentence)
                            words1.extend(w)
                            docs.append((w, each_category))
                    # stem and lower each word and remove duplicates
                    words1 = [stemmer.stem(w.lower()) for w in words1]
                    words1 = sorted(list(set(words1)))
                    # create our training data
                    training = []
                    output = []
                    # create an empty array for our output
                    output_empty = [0] * len(categories)
                                    
                                    
                    for doc in docs:
                        # initialize our bag of words(bow) for each document in the list
                        bow = []
                        # list of tokenized words for the pattern
                        token_words = doc[0]
                        # stem each word
                        token_words = [stemmer.stem(word.lower()) for word in token_words]
                        # create our bag of words array
                        for w in words1:
                            bow.append(1) if w in token_words else bow.append(0)
                                        
                        output_row = list(output_empty)
                        output_row[categories.index(doc[1])] = 1
                                        
                        # our training set will contain a the bag of words model and the output row that tells which catefory that bow belongs to.
                        training.append([bow, output_row])
                                    
                    # shuffle our features and turn into np.array as tensorflow  takes in numpy array
                    random.shuffle(training)
                    training = np.array(training)
                    # NOW DIVING INTO TENSORFLOW
                                    
                    # trainX contains the Bag of words and train_y contains the label/ category
                    train_y = list(training[:,1])
                    train_x = list(training[:,0])
                    

                    # reset underlying graph data
                    tf.reset_default_graph()
                    # Build neural network
                    net = tflearn.input_data(shape=[None, len(train_x[0])])
                    net = tflearn.fully_connected(net, 8)
                    net = tflearn.fully_connected(net, 8)
                    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
                    net = tflearn.regression(net)
                                    
                    # Define model and setup tensorboard
                    model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
                    # Start training (apply gradient descent algorithm)
                    model.fit(train_x, train_y, n_epoch=1000, batch_size=None, show_metric=True, shuffle=True)
                    model.save('model.tflearn')

                    
                    result=str(categories[np.argmax(model.predict([get_tf_record(sentence)]))])
                    if lang=='en':
                        file_temp.write("Based on our analysis, you should consult a "+result)
                    else:
                        output_text=TextBlob("Based on our analysis, you should consult a "+result)
                        output_text=output_text.translate(to=lang)
                        file_temp.write(output_text)
                    break
    file_temp.close()