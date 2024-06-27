#!/usr/bin/env python
# coding: utf-8

# In[54]:


import pandas as pd
import json
from datetime import date, timedelta


# In[55]:


config_file_path = r'.\..\smart-shifts-system\config.json'
f = open('config.json')
data = json.load(f)

starting_day = data['starting_day']
starting_month = data['starting_month']
ending_day = data['ending_day']
ending_month = data['ending_month']


# In[64]:


df = pd.read_csv(r'.\..\smart-shifts-system\shifts-form.csv')
df = df.drop(columns=['חותמת זמן'])


# In[57]:


def create_shift_dates_array(starting_day, ending_day, starting_month, ending_month):
    start_date = date(2024, starting_month, starting_day) 
    end_date = date(2024, ending_month, ending_day)    # perhaps date.now()

    shift_array = []
    
    delta = end_date - start_date   # returns timedelta

    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        shift_array.append(f'{day.day}.{day.month} Day Shift')
        shift_array.append(f'{day.day}.{day.month} Night Shift')
        
    return shift_array


# In[58]:


def init_shifts_ava_df(index, columns):

    shifts_ava_df = pd.DataFrame(index = index, columns = columns)

    for name in shifts_ava_df.columns:
        for shift in shifts_ava_df.index:
            shifts_ava_df.loc[shift, name] = name

    return shifts_ava_df


# In[65]:


df


# In[66]:


def create_unavailability_shifts_df(df, starting_day,ending_day,starting_month,ending_month):
    index = create_shift_dates_array(starting_day,ending_day,starting_month,ending_month)
    columns = df['Name']
    
    unava_shifts_df = pd.DataFrame(index = index, columns = columns)
    ava_shifts_df = init_shifts_ava_df(index,columns)

    for index, name in enumerate(columns):
        unava_shifts_df.loc[:, name] = ''
        if type(df.loc[index, 'Unavailable'])==type(' '):
            for shift in df.loc[index, 'Unavailable'].split(', '):
                unava_shifts_df.loc[shift, name] = 'x'
                ava_shifts_df.loc[shift,name] = ''
                
    return unava_shifts_df, ava_shifts_df


# In[67]:


shifts_unava_df, shifts_ava_df = create_unavailability_shifts_df(df, starting_day,ending_day,starting_month,ending_month)

shifts_unava_df.to_excel('shfits_unavailability.xlsx')
shifts_ava_df.to_excel('shifts_availability.xlsx')


# In[62]:


shifts_ava_df


# In[61]:


print("DONE")


# In[53]:


get_ipython().system('jupyter nbconvert --to script convert_excel_to_better_excel.ipynb')


# In[ ]:




