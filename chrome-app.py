# -*- coding: utf-8 -*-


import pandas as pd
from textblob import TextBlob
import streamlit as st

#from textblob.sentiments import NaiveBayesAnalyzer



st.title("User--Review")
uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    st.write(df.head())
    
    
    
    df_star_below_4 = df.loc[(df['Star'] <= 3)]#taking those rows whose rating is 3 and less
    text = df_star_below_4[['ID','Text','Star']] #taking only id and review column
    #text_dict = dict(zip(df_star_below_4.ID,df_star_below_4.Text))
        
    p_words=pd.read_csv('positive_words.txt',header = None)# reading the positive words
    #p_words_list = p_words.values.tolist()#converting it to list
    p_words.columns = ['Positive words']
    p_words = p_words['Positive words'].tolist()
     
    p_text=[]
    p_id = []
    p_star = []
    
    
    
    
    for item in text.index:# iterate through the dictionary for getting text
        
        split_sentence = text['Text'][item].split(" ") #split the review to each word 
        split_sentence= [each_word.lower() for each_word in split_sentence] #converting it to lower case
    
        for word in split_sentence:
    
            for p_word in p_words:
    
                if word == p_word:
                    if text['ID'][item] not in p_id:
                        key = text['ID'][item]
                        value = text['Text'][item]
                        star = text['Star'][item]
                        p_text.append(value)
                        p_id.append(key)
                        p_star.append(star)
    
    df_p_text = pd.DataFrame(list(zip(p_id,p_text,p_star)),columns=['Id','Text','Star'])
    #dictionary = dict(zip(p_id, p_text))
    
    
    
    
    
    #def Polarity(sent):
    #    s = ''
    #    for wd in sent:
    #        if wd.isalpha() == True:
    #            s = s +' '+ wd
    #    
    #    blob = TextBlob(sent, analyzer=NaiveBayesAnalyzer())
    #    senti = print(blob.sentiment)
    #    return senti
    
    
    
    #num_words = len(real)
    #num_p_words = 0
    #for wd in real:
    #    for p_word in p_words:
    #        if wd == p_word:
    #            num_p_words = num_p_words+1
    #            print(wd)
    #multi = num_p_words/num_words
    #polarity = (num_p_words*multi)/num_words
    #    return polarity
        
    
                    
    n = st.sidebar.slider(label = 'Polarity',min_value = 0.1,max_value = 0.99,step = 0.01)    
    
    i = 0
    id_list = []
    pol = []
    for r in df_p_text.index:
    #    print(df_p_text['Text'][r])
    #    print(df_p_text['Id'][r])
    #    print(df_p_text['Text'][r])
        text = TextBlob(df_p_text['Text'][r])
        polarity = text.sentiment[0]
        if polarity>n:
            
    #        print(df_p_text['Id'][r],df_p_text['Star'][r],df_p_text['Text'][r])
            id_list.append(df_p_text['Id'][r])
            pol.append(polarity)
            i = i+1
    #            print(i)
    
    final_rows = df[df['ID'].isin(id_list)]
        
    final_rows['Polarity'] = pol
    #    print(final_rows[['ID','Text','Star','Polarity']])
    st.write('The ID and Review of the user who has given positive comments \nbut rated 3 or below.')
    st.write(i,' user have given positive review but rated 3 or below.')
    st.write(final_rows[['ID','Text','Star','Polarity']])    


else:
    st.write('File Not Found')
    



