# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 21:25:12 2025

@author: ranja
"""
import streamlit as st
import preprocessing
import helper
import matplotlib.pyplot as plt


st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df= preprocessing.preprocess(data)
    
    st.dataframe(df)
   
    
    #fetch unique users
    user_list=df['user'].unique().tolist()
 
    user_list.sort()
    user_list.insert(0,"overall")
    
    
    selected_user = st.sidebar.selectbox("show analyst wrt",user_list)
    
   
    
if st.sidebar.button("Show Analysis"):
    
    num_messages,words,num_media,num_links= helper.fetch_stats(selected_user,df)
    st.title("top Statistics")
    col1,col2,col3,col4= st.columns(4)
        
    with col1:
      st.header("Total Messages")
      st.title(num_messages)
            
    with col2:
      st.header("Total Words")
      st.title(words)
        
    with col3:
      st.header("media shared")
      st.title(num_media)
            
    with col4:
      st.header("links shared")
      st.title(num_links)
             
             
    #timeline
    st.subheader("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user, df)

    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)       
             
    #activity map
    st.title('Activity Map')
    col1,col2=st.columns(2)
    
    with col1:
        st.header("Most Busy Day")
        busy_day=helper.week_activity_map(selected_user, df)
        fig,ax=plt.subplots()
        ax.bar(busy_day.index,busy_day.values,color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
    with col2:
        st.header("Most Busy Month")
        busy_month=helper.monthly_activity_map(selected_user, df)
        fig,ax=plt.subplots()
        ax.bar(busy_month.index,busy_month.values,color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    
           
             
        
    #finding the busiest users in group 
    if selected_user=='overall':
          st.title('Most Busiest Users')
          x,new_df =helper.most_busy_users(df)
            #fig,ax=plt.subplots()
            
            
          col1,col2=st.columns(2)
        
          with col1:
             st.subheader("Bar Chart")
             fig, ax = plt.subplots()
             ax.bar(x.index, x.values)
             plt.xticks(rotation='vertical')
             st.pyplot(fig)
             
          with col2:
        
             st.subheader("User Percentage")
             st.dataframe(new_df)
           
           
    # Show WordCloud
    st.subheader("Word Cloud")
    df_wc = helper.create_wordcloud(selected_user, df)

    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    ax.axis("off")
    st.pyplot(fig)
            
     # Most Common Words
    st.subheader("Most Common Words")
    most_common_df = helper.most_common_words(selected_user, df)

    fig, ax = plt.subplots()
    ax.bar(most_common_df[0], most_common_df[1])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
      
            
            
            
        
       
        
       
    
     