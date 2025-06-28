# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 21:34:13 2025

@author: ranja
"""

# processing.py
import re
import pandas as pd


def preprocess(data):
    # Regex pattern to extract date, time, user, message
    pattern = r"(\d{2}/\d{2}/\d{2}),\s*(\d{1,2}:\d{2}\s*[ap]m)\s*-\s*([^:]+?):\s*(.+)"
    matches = re.findall(pattern, data)

    # Create DataFrame
    df = pd.DataFrame(matches, columns=['date_str', 'time_str', 'user_raw', 'message_raw'])

    # Combine and convert to datetime
    df['date'] = pd.to_datetime(df['date_str'] + ' ' + df['time_str'], format='%d/%m/%y %I:%M %p')

    # Clean message and user fields
    df['user'] = df['user_raw'].str.strip()
    df['message'] = df['message_raw'].str.strip()

    # Extract date/time parts
    df['year'] = df['date'].dt.year
    df['month_num']=df['date'].dt.month
    df['month'] = df['date'].dt.strftime('%B')
    df['day'] = df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Final columns
    df = df[['date', 'user', 'message', 'year', 'month_num', 'month', 'day','day_name', 'hour', 'minute']]
    return df


   