# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 21:32:14 2025

@author: ranja
"""
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
    
def fetch_stats(selected_user, df):
    if selected_user.lower() == 'overall':
        temp = df
    else:
        temp = df[df['user'].str.lower().str.strip() == selected_user.lower().strip()]

    num_messages = temp.shape[0]
    num_words = sum(len(msg.split()) for msg in temp['message'])

    num_media = temp[temp['message'] == '<Media omitted>'].shape[0]
    
    num_links = temp['message'].str.contains('http|www', case=False).sum()

    return num_messages, num_words, num_media,num_links

  
def most_busy_users(df):
    #df = df[df['user'] != 'group_notification']
    x=df['user'].value_counts().head(11)
    df=round((df['user'].value_counts().head(11)/df.shape[0])*100,2).reset_index().rename(columns={'count':'percentage'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user!='overall':
     df=df[df['user']==selected_user]
     
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user,df):
    with open("stop_hinglish.txt","r") as f:
       stop_words = f.read()
    if selected_user!="overall":
        
        df=df[df['user']==selected_user]
        
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>']
        
    words=[]
    for message in temp['message']:
      for word in message.lower().split():
          if word not in stop_words:
              words.append(word)
                
    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df
            


def monthly_timeline(selected_user,df):
    if selected_user!="overall":        
        df=df[df['user']==selected_user]
    
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
        
    timeline['time']=time   
       
    return timeline     
        
def week_activity_map(selected_user,df):
    if selected_user!="overall":        
        df=df[df['user']==selected_user]
        
    return df['day_name'].value_counts()

def monthly_activity_map(selected_user,df):
    if selected_user!="overall":        
        df=df[df['user']==selected_user]
        
    return df['month'].value_counts()
    
   