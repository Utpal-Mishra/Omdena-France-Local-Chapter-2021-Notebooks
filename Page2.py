import streamlit as st
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import plotly.express as px
from datetime import datetime as dt

st.title("COVID-19 BEFORE-DURING ANALYSIS IN FRANCE")

st.header("PART 2")

st.subheader("Master Data")

"Loading the Master Data...."

label = st.empty()
bar = st.progress(0)

for i in range(100):
    # Update progress bar with iterations
    label.text(f'Loaded {i+1} %')
    bar.progress(i+1)
    time.sleep(0.01)

path = 'new_master_data.csv'
data = pd.read_csv(path)
#print("Data Shape: ", data.shape)
data.head()

".... and now we're done again!!!"

# Plot Function
def barplot(data, x, y, frame, color, ylabel, title):
  fig = px.bar(pollutants, x=x, y=y, animation_frame = frame, color=color, barmode='group')
  fig.update_xaxes(title_text = "France Cities", rangeslider_visible=True, showline=True, linewidth=2, linecolor='black', mirror=True)
  fig.update_yaxes(title_text = ylabel, showline=True, linewidth=2, linecolor='black', mirror=True)
  # fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
  fig.update_layout(height=700, width=1400, title_text=title) 
  st.plotly_chart(fig)
  
st.subheader("Visualization Part 1")
  
### MEDIAN
median = data[["date", "City", "('median', 'co')", "('median', 'dew')", "('median', 'humidity')",
       "('median', 'no2')", "('median', 'o3')", "('median', 'pm10')",
       "('median', 'pm25')", "('median', 'pressure')", "('median', 'so2')",
       "('median', 'temperature')", "('median', 'wind gust')",
       "('median', 'wind speed')"]]

# print("Data Shape: ", median.shape)

pollutants = median[["date", "City", "('median', 'co')", "('median', 'dew')", "('median', 'no2')", "('median', 'o3')", "('median', 'pm10')", "('median', 'pm25')", "('median', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("1.1. Show Plot with Average Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Average Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France from 2019-20"))

### MAX
max = data[["date", "City", "('max', 'co')", "('max', 'dew')", "('max', 'humidity')",
       "('max', 'no2')", "('max', 'o3')", "('max', 'pm10')",
       "('max', 'pm25')", "('max', 'pressure')", "('max', 'so2')",
       "('max', 'temperature')", "('max', 'wind gust')",
       "('max', 'wind speed')"]]

#print("Data Shape: ", max.shape)

pollutants = max[["date", "City", "('max', 'co')", "('max', 'dew')", "('max', 'no2')", "('max', 'o3')", "('max', 'pm10')", "('max', 'pm25')", "('max', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("1.2. Show Plot with Maximum Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Maximum Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France from 2019-20"))

### MIN
min = data[["date", "City", "('min', 'co')", "('min', 'dew')", "('min', 'humidity')",
       "('min', 'no2')", "('min', 'o3')", "('min', 'pm10')",
       "('min', 'pm25')", "('min', 'pressure')", "('min', 'so2')",
       "('min', 'temperature')", "('min', 'wind gust')",
       "('min', 'wind speed')"]]

#print("Data Shape: ", min.shape)

pollutants = min[["date", "City", "('min', 'co')", "('min', 'dew')", "('min', 'no2')", "('min', 'o3')", "('min', 'pm10')", "('min', 'pm25')", "('min', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("1.3. Show Plot with Minimum Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Minimum Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France from 2019-20"))


st.subheader("Visualization Part 2: No Lockdown Phase")

## NO LOCKDOWN PHASE

### MEDIAN
median = data[["date", "City", "('median', 'co')", "('median', 'dew')", "('median', 'humidity')",
       "('median', 'no2')", "('median', 'o3')", "('median', 'pm10')",
       "('median', 'pm25')", "('median', 'pressure')", "('median', 'so2')",
       "('median', 'temperature')", "('median', 'wind gust')",
       "('median', 'wind speed')"]]

# print("Data Shape: ", median.shape)

pollutants = median[["date", "City", "('median', 'co')", "('median', 'dew')", "('median', 'no2')", "('median', 'o3')", "('median', 'pm10')", "('median', 'pm25')", "('median', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("2.1.1. Show Plot with Average Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Average Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France from 2020-21 during No Lockdown"))

### MAX
max = data[["date", "City", "('max', 'co')", "('max', 'dew')", "('max', 'humidity')",
       "('max', 'no2')", "('max', 'o3')", "('max', 'pm10')",
       "('max', 'pm25')", "('max', 'pressure')", "('max', 'so2')",
       "('max', 'temperature')", "('max', 'wind gust')",
       "('max', 'wind speed')"]]

#print("Data Shape: ", max.shape)

pollutants = max[["date", "City", "('max', 'co')", "('max', 'dew')", "('max', 'no2')", "('max', 'o3')", "('max', 'pm10')", "('max', 'pm25')", "('max', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("2.1.2. Show Plot with Maximum Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Maximum Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France in 2020-21 during No Lockdown"))

### MIN
min = data[["date", "City", "('min', 'co')", "('min', 'dew')", "('min', 'humidity')",
       "('min', 'no2')", "('min', 'o3')", "('min', 'pm10')",
       "('min', 'pm25')", "('min', 'pressure')", "('min', 'so2')",
       "('min', 'temperature')", "('min', 'wind gust')",
       "('min', 'wind speed')"]]

#print("Data Shape: ", min.shape)

pollutants = min[["date", "City", "('min', 'co')", "('min', 'dew')", "('min', 'no2')", "('min', 'o3')", "('min', 'pm10')", "('min', 'pm25')", "('min', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("2.1.3. Show Plot with Minimum Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Minimum Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France from 2020-21 during No Lockdown"))


st.subheader("Visualization Part 2: 1st Lockdown Phase")

## 1st LOCKDOWN PHASE

### MEDIAN
median = data[["date", "City", "('median', 'co')", "('median', 'dew')", "('median', 'humidity')",
       "('median', 'no2')", "('median', 'o3')", "('median', 'pm10')",
       "('median', 'pm25')", "('median', 'pressure')", "('median', 'so2')",
       "('median', 'temperature')", "('median', 'wind gust')",
       "('median', 'wind speed')"]]

# print("Data Shape: ", median.shape)

pollutants = median[["date", "City", "('median', 'co')", "('median', 'dew')", "('median', 'no2')", "('median', 'o3')", "('median', 'pm10')", "('median', 'pm25')", "('median', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("2.2.1. Show Plot with Average Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Average Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France from 2020 during 1st Lockdown"))

### MAX
max = data[["date", "City", "('max', 'co')", "('max', 'dew')", "('max', 'humidity')",
       "('max', 'no2')", "('max', 'o3')", "('max', 'pm10')",
       "('max', 'pm25')", "('max', 'pressure')", "('max', 'so2')",
       "('max', 'temperature')", "('max', 'wind gust')",
       "('max', 'wind speed')"]]

#print("Data Shape: ", max.shape)

pollutants = max[["date", "City", "('max', 'co')", "('max', 'dew')", "('max', 'no2')", "('max', 'o3')", "('max', 'pm10')", "('max', 'pm25')", "('max', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("2.2.2. Show Plot with Maximum Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Maximum Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France in 2020 during 1st Lockdown"))

### MIN
min = data[["date", "City", "('min', 'co')", "('min', 'dew')", "('min', 'humidity')",
       "('min', 'no2')", "('min', 'o3')", "('min', 'pm10')",
       "('min', 'pm25')", "('min', 'pressure')", "('min', 'so2')",
       "('min', 'temperature')", "('min', 'wind gust')",
       "('min', 'wind speed')"]]

#print("Data Shape: ", min.shape)

pollutants = min[["date", "City", "('min', 'co')", "('min', 'dew')", "('min', 'no2')", "('min', 'o3')", "('min', 'pm10')", "('min', 'pm25')", "('min', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("2.2.3. Show Plot with Minimum Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Minimum Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France in 2020 during 1st Lockdown"))


st.subheader("Visualization Part 2: 2nd Lockdown Phase")

## 2nd LOCKDDOWN PHASE

### MEDIAN
median = data[["date", "City", "('median', 'co')", "('median', 'dew')", "('median', 'humidity')",
       "('median', 'no2')", "('median', 'o3')", "('median', 'pm10')",
       "('median', 'pm25')", "('median', 'pressure')", "('median', 'so2')",
       "('median', 'temperature')", "('median', 'wind gust')",
       "('median', 'wind speed')"]]

# print("Data Shape: ", median.shape)

pollutants = median[["date", "City", "('median', 'co')", "('median', 'dew')", "('median', 'no2')", "('median', 'o3')", "('median', 'pm10')", "('median', 'pm25')", "('median', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("2.3.1. Show Plot with Average Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Average Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France in 2020 during 2nd Lockdown"))

### MAX
max = data[["date", "City", "('max', 'co')", "('max', 'dew')", "('max', 'humidity')",
       "('max', 'no2')", "('max', 'o3')", "('max', 'pm10')",
       "('max', 'pm25')", "('max', 'pressure')", "('max', 'so2')",
       "('max', 'temperature')", "('max', 'wind gust')",
       "('max', 'wind speed')"]]

#print("Data Shape: ", max.shape)

pollutants = max[["date", "City", "('max', 'co')", "('max', 'dew')", "('max', 'no2')", "('max', 'o3')", "('max', 'pm10')", "('max', 'pm25')", "('max', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("2.3.2. Show Plot with Maximum Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Maximum Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France in 2020 during 2nd Lockdown"))

### MIN
min = data[["date", "City", "('min', 'co')", "('min', 'dew')", "('min', 'humidity')",
       "('min', 'no2')", "('min', 'o3')", "('min', 'pm10')",
       "('min', 'pm25')", "('min', 'pressure')", "('min', 'so2')",
       "('min', 'temperature')", "('min', 'wind gust')",
       "('min', 'wind speed')"]]

#print("Data Shape: ", min.shape)

pollutants = min[["date", "City", "('min', 'co')", "('min', 'dew')", "('min', 'no2')", "('min', 'o3')", "('min', 'pm10')", "('min', 'pm25')", "('min', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("2.3.3. Show Plot with Minimum Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Minimum Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France in 2020 during 2nd Lockdown"))


st.subheader("Visualization Part 2: 3rd Lockdown Phase")

## 3rd LOCKDOWN PHASE

### MEDIAN
median = data[["date", "City", "('median', 'co')", "('median', 'dew')", "('median', 'humidity')",
       "('median', 'no2')", "('median', 'o3')", "('median', 'pm10')",
       "('median', 'pm25')", "('median', 'pressure')", "('median', 'so2')",
       "('median', 'temperature')", "('median', 'wind gust')",
       "('median', 'wind speed')"]]

# print("Data Shape: ", median.shape)

pollutants = median[["date", "City", "('median', 'co')", "('median', 'dew')", "('median', 'no2')", "('median', 'o3')", "('median', 'pm10')", "('median', 'pm25')", "('median', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("2.4.1. Show Plot with Average Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Average Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France in 2021 during 3rd Lockdown"))

### MAX
max = data[["date", "City", "('max', 'co')", "('max', 'dew')", "('max', 'humidity')",
       "('max', 'no2')", "('max', 'o3')", "('max', 'pm10')",
       "('max', 'pm25')", "('max', 'pressure')", "('max', 'so2')",
       "('max', 'temperature')", "('max', 'wind gust')",
       "('max', 'wind speed')"]]

#print("Data Shape: ", max.shape)

pollutants = max[["date", "City", "('max', 'co')", "('max', 'dew')", "('max', 'no2')", "('max', 'o3')", "('max', 'pm10')", "('max', 'pm25')", "('max', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("2.4.2. Show Plot with Maximum Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Maximum Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France in 2021 during 3rd Lockdown"))

### MIN
min = data[["date", "City", "('min', 'co')", "('min', 'dew')", "('min', 'humidity')",
       "('min', 'no2')", "('min', 'o3')", "('min', 'pm10')",
       "('min', 'pm25')", "('min', 'pressure')", "('min', 'so2')",
       "('min', 'temperature')", "('min', 'wind gust')",
       "('min', 'wind speed')"]]

#print("Data Shape: ", min.shape)

pollutants = min[["date", "City", "('min', 'co')", "('min', 'dew')", "('min', 'no2')", "('min', 'o3')", "('min', 'pm10')", "('min', 'pm25')", "('min', 'so2')"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
pollutants.sort_values(["date", "Pollutants"], inplace = True)
pollutants.head()

if st.checkbox("2.4.3. Show Plot with Minimum Concentration of Pollutants"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "Pollutants", 
        "Minimum Concentration of Pollutants (Unit - µg/m³)", 
        "Air Pollutants in France in 2021 during 3rd Lockdown"))


st.subheader("Visualization Part 3: No Lockdown Phase")

# CO2

## NO LOCKDOWN PHASE
lockdown = data[data.lockdown == "No lockdown"].reset_index().drop('index', axis = 1)
print("Data Shape: ", lockdown.shape)
# From: 2020-02-15
# To  : 2020-03-17

# From: 2020-05-10
# To  : 2020-10-17

# From: 2020-12-14
# To  : 2021-02-26

# From: 2021-05-02
# To  : 2021-07-27

pollutants = lockdown[["date", "City", "driving", "transit", "walking"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "CO2 Sources", value_name = "Concentration")
pollutants.sort_values(["date", "CO2 Sources"], inplace = True)
pollutants.head()

if st.checkbox("3.1. Show Plot with Average Concentration of CO2 Sources"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "CO2 Sources", 
        "Average Concentration of CO2 Sources (Unit - µg/m³)", 
        "Air Pollutants in France from 2020-21 during No Lockdown"))


st.subheader("Visualization Part 3: 1st Lockdown Phase")

## 1st LOCKDOWN PHASE
lockdown = data[data.lockdown == "lockdown_1"].reset_index().drop('index', axis = 1) 
print("Data Shape: ", lockdown.shape)
# From: 2020-03-17
# To  : 2020-05-10

pollutants = lockdown[["date", "City", "driving", "transit", "walking"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "CO2 Sources", value_name = "Concentration")
pollutants.sort_values(["date", "CO2 Sources"], inplace = True)
pollutants.head()

if st.checkbox("3.2. Show Plot with Average Concentration of CO2 Sources"):   
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "CO2 Sources", 
        "Average Concentration of CO2 Sources (Unit - µg/m³)", 
        "Air Pollutants in France in 2020 during 1st Lockdown"))


st.subheader("Visualization Part 3: 2nd Lockdown Phase")

## 2nd LOCKDOWN PHASE
lockdown = data[data.lockdown == "lockdown_2"].reset_index().drop('index', axis = 1)
print("Data Shape: ", lockdown.shape)
# From: 2020-10-17
# To  : 2020-12-14

pollutants = lockdown[["date", "City", "driving", "transit", "walking"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "CO2 Sources", value_name = "Concentration")
pollutants.sort_values(["date", "CO2 Sources"], inplace = True)
pollutants.head()

if st.checkbox("3.3. Show Plot with Average Concentration of CO2 Sources"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "CO2 Sources", 
        "Average Concentration of CO2 Sources (Unit - µg/m³)", 
        "Air Pollutants in France in 2020 during 2nd Lockdown"))


st.subheader("3.2.1. Visualization Part 3: 3rd Lockdown Phase")

## 3rd LOKDOWN PHASE
lockdown = data[data.lockdown == "lockdown_3"].reset_index().drop('index', axis = 1)
print("Data Shape: ", lockdown.shape)
# From: 2021-02-26
# To  : 2021-05-02

pollutants = lockdown[["date", "City", "driving", "transit", "walking"]]

pollutants = pollutants.melt(id_vars=["date", "City"], var_name = "CO2 Sources", value_name = "Concentration")
pollutants.sort_values(["date", "CO2 Sources"], inplace = True)
pollutants.head()

if st.checkbox("3.4. Show Plot with Average Concentration of CO2 Sources"):    
    # data
    st.write(barplot(pollutants, 
        "City", 
        "Concentration", 
        "date", 
        "CO2 Sources", 
        "Average Concentration of CO2 Sources (Unit - µg/m³)", 
        "Air Pollutants in France in 2021 during 3rd Lockdown"))