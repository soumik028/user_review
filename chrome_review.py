# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 19:40:37 2021

@author: dasso
"""

import pandas as pd 
import streamlit as st
  
import os
st.title("Review")



def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

filename = file_selector()
st.write('You selected `%s`' % filename)









# creating a data frame 
#filename  = 'chrome_reviews.csv'
df = pd.read_csv(filename) #reading the file
st.write(df.head())



df_star_below_4 = df.loc[(df['Star'] <= 3)]#taking those rows whose rating is 3 and less


p_words=pd.read_csv('positive_words.txt')# reading the positive words
p_words_list = p_words.values.tolist()#converting it to list

text = df_star_below_4[['ID','Text']] #taking only id and review column
text_dict = dict(zip(df_star_below_4.ID,df_star_below_4.Text))# making it a dictionary
id_list=[]

for item in text_dict.items():# iterate through the dictionary for getting text
    s = item[1].split(" ") #split the text to each word 
    s= [each_word.lower() for each_word in s] #converting it to lower case
    for word in p_words_list:#iterating through positive words
        if (s == word): #checking if the positive word matches with the word in the text(review)
            id_list.append(item[0]) #if it matches then append the empty list with ID of that review row
#            print(s,word,item[0])
final_review=[]        
for i in id_list:  #iterate thorugh the ids 
    review = df.loc[df['ID']== i ] # getting the rows having those id
    review = review[['ID','Text','Star']].values.tolist() #getting the Id original Text and user name of those Ids and converting it to list
    final_review.append(review) #appending the empty list

final_review = pd.DataFrame(final_review,columns = ['ID Review Star'])
st.write('The ID and Review of the user who has given positive comments \nbut rated 3 or below.')
st.write(len(final_review),' user have given positive review but rated 3 or below.')
st.write(final_review)    

    
#print("The ids which have a positive review but rating is 3 or less are as follows ",id_list)

    



