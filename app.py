import streamlit as st
import time

import sys
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import plotly.express as px
from datetime import datetime as dt


sys.setrecursionlimit(100000)
#print("Installed Dependencies")


# Add text and data
### Add title
st.title("COVID-19 BEFORE-DURING ANALYSIS IN FRANCE")

st.header("PART 1")

st.subheader("Loading the COVID-19 Data....")

label = st.empty()
bar = st.progress(0)

for i in range(100):
    # Update progress bar with iterations
    label.text(f'Loaded {i+1} %')
    bar.progress(i+1)
    time.sleep(0.01)

path = 'COVID_2020.csv'
data = pd.read_csv(path)
data = data.drop("Unnamed: 0", axis = 1)
#print("Data Shape: ", data.shape)
#data.head()

".... and now we're done!!!"

SpecieClass = []
for i in data.Specie:
  if i=="co":
    SpecieClass.append(1)
  if i=="no2":
    SpecieClass.append(2)
  if i=="o3":
    SpecieClass.append(3)
  if i=="pm1":
    SpecieClass.append(4)
  if i=="pm10":
    SpecieClass.append(5)
  if i=="pm25":
    SpecieClass.append(6)
  if i=="so2":
    SpecieClass.append(7)

data["Class"] = SpecieClass

if st.checkbox("Show DataFrame"):    
    # data
    st.write(data.head())


data = data[data.Country == "FR"]
print("France Data Dimensions: ", data.shape)
#st.text("France Data Dimensions: ", data.shape)

st.header("Data Visualization")

st.subheader("Scatter Plot")

# Scatter Plot
if st.checkbox("Average Proportion of Pollutants"):  
    fig = px.scatter(data, x="count", y="median", animation_frame="Date", animation_group="Specie", size=data["count"], color="Specie", hover_name="Specie", facet_col="Specie")
    fig.update_xaxes(title_text = "count", rangeslider_visible=False, showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_yaxes(title_text = "Average Concentration", showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_layout(height=450, width=1200, title_text="Average Concentration (Unit - µg/m³) of Air Pollutants in France from 2019-20") 
    #fig.show()
    st.plotly_chart(fig)    

# Scatter Plot
if st.checkbox("Average Concentration of Pollutants"): 
    fig = px.scatter(data, x="Specie", y="median", animation_frame="Date", size=data["count"], color="City", hover_name="Specie", facet_col="Specie")
    fig.update_xaxes(title_text = "Specie", rangeslider_visible=False, showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_yaxes(title_text = "Average Concentration", showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_layout(height=450, width=1200, title_text="Average Concentration (Unit - µg/m³) of Air Pollutants in France from 2019-20") 
    #fig.show()
    st.plotly_chart(fig)  


st.subheader("Bar Plot")

# Bar Plot
if st.checkbox("Average Concentration of Species in Cities of France"):   
    fig = px.bar(data, x="City", y="median", animation_frame = "Date", color='Specie', barmode='group')
    fig.update_xaxes(title_text = "France Cities", rangeslider_visible=False, showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_yaxes(title_text = "Average Concentration of Pollutants (Unit - µg/m³)", showline=True, linewidth=2, linecolor='black', mirror=True)
    # fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
    fig.update_layout(height=600, width=1400, title_text="Air Pollutants in France from 2019-20") 
    #fig.show()
    st.plotly_chart(fig) 


# MAP
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import random # library for random number generation
import matplotlib.cm as cm
import matplotlib.colors as colors
#%matplotlib inline 

#!conda install -c conda-forge geopy --yes 
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 
    
import requests # library to handle requests
import json # library to handle JSON files
from pandas import json_normalize # tranform JSON file into a pandas dataframe

#!conda install -c conda-forge folium=0.5.0 --yes
import folium # plotting library
from folium import plugins
from streamlit_folium import folium_static
import leafmap
#from streamlit_folium import folium_static

City = []
Longitude = []
Latitude = []

for i in data.City.unique():
  geolocator = Nominatim(user_agent="four_square")
  location = geolocator.geocode(i+", France")
  latitude = location.latitude
  longitude = location.longitude
  City.append(i)
  Longitude.append(longitude)
  Latitude.append(latitude)
  # print(i, longitude, latitude)

# data["Longitude"] = Longitude
# data["Latitude"] = Latitude

Coordinates = pd.DataFrame({"City": City,
               "Longitude": Longitude,
               "Latitude": Latitude})

st.subheader("Folium Map Plots")

if st.checkbox("Show Coordinates DataFrame"):    
    # data
    st.write(Coordinates.head())

# Coordinates.head()
newdata = pd.merge(data, Coordinates, on='City', how='outer')
# print("Dimensions of New Data: ", newdata.shape)

def map(data):
  fig = px.scatter_geo(data, 
                     lat='Latitude', 
                     lon='Longitude', 
                     size='median', 
                     animation_frame="Date", 
                     animation_group = "Specie",
                     title='Air Pollutants Concentration (Unit - µg/m³) throughout Cities in France', 
                     hover_name="City",
                     projection = "orthographic", 
                     width = 1400,
                     height = 600, 
                     color = "City")
  fig.update(layout_coloraxis_showscale=False)
  #fig.show()
  st.plotly_chart(fig)
  

if st.checkbox("Orthographic Plot representing Concentration of Air Pollutants"): 
    map(newdata)

address = 'France'

geolocator = Nominatim(user_agent="four_square")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of France are {}, {}.'.format(latitude, longitude))


# midpoint = (np.average(newdata['Latitude']), np.average(newdata['Longitude']))
if st.checkbox("Locate France"):
    Map = folium.Map(location = [latitude, longitude], zoom_start = 12, tiles = 'Stamen Terrain') #Mapbox Bright #Stamen Toner
    Marker = folium.map.FeatureGroup()
    Marker.add_child(folium.CircleMarker([latitude, longitude], 
                                                 radius = 5, 
                                                 color = 'red', 
                                                 fill_color = 'Red'))
    Map.add_child(Marker)
    folium.Marker([latitude, longitude], popup = 'France').add_to(Map)
    folium_static(Map)


if st.checkbox("Identify Cities in France"):
    # create map of france using latitude and longitude values
    Map = folium.Map(location=[latitude, longitude], zoom_start=6)
    
    # add markers to map
    for lat, lng, reg in zip(newdata.Latitude, newdata.Longitude, newdata.City):
        label = '{}, France'.format(reg)
        label = folium.Popup(label, parse_html=True)
        folium.CircleMarker(
            [lat, lng],
            radius=10,
            popup=label,
            color='blue',
            fill=True,
            fill_color='#3186cc',
            fill_opacity=0.7,
            parse_html=False).add_to(Map)  
    
    folium_static(Map)

if st.checkbox("Locate Cities in France"):
    Map = folium.Map(location = [latitude, longitude], zoom_start = 6)
    
    # instantiate a mark cluster object for the incidents in the dataframe
    incidents = plugins.MarkerCluster().add_to(Map)
    
    # loop through the dataframe and add each data point to the mark cluster
    for lat, lng, label, in zip(newdata.Latitude, newdata.Longitude, newdata.City):
        folium.Marker(
            location=[lat, lng],
            icon=None,
            popup=label,
        ).add_to(incidents)
    
    # display map
    folium_static(Map)
    

if st.checkbox("Total Proportions of Pollutants in Cities of France"):
    Map = folium.Map(location=[latitude, longitude], zoom_start=6)
    
    # instantiate a feature group in the dataframe
    group = plugins.MarkerCluster().add_to(Map) # folium.map.FeatureGroup()
    
    # loop through the 100 crimes and add each to the incidents feature group
    for lat, lng, in zip(newdata.Latitude, newdata.Longitude):
        group.add_child(
            folium.CircleMarker(
                [lat, lng],
                radius=5, # define how big you want the circle markers to be
                color='yellow',
                fill=True,
                fill_color='blue',
                fill_opacity=0.6
            )
        )
    
    # add pop-up text to each marker on the map
    latitudes = list(newdata.Latitude)
    longitudes = list(newdata.Longitude)
    labels = list(newdata.City)
    
    for lat, lng, label in zip(latitudes, longitudes, labels):
        folium.Marker([lat, lng], popup=label).add_to(Map)    
        
    # add group to map
    Map.add_child(group)
    
    # display map
    folium_static(Map)



##############################################################################
##############################################################################
##############################################################################



st.header("PART 2")

st.subheader("Loading the Master Data....")

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


st.subheader("Visualization Part 3: 3rd Lockdown Phase")

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
    
    

##############################################################################
##############################################################################
##############################################################################



def plot(city):
  fig = go.Figure()
  fig.add_trace(go.Scatter(x = max[max.City == city].date, y = max[max.City == city].Concentration, name = "max conc.", mode = "lines", line=dict(color='blue')))
  fig.add_trace(go.Scatter(x = min[min.City == city].date, y = min[min.City == city].Concentration, name = "min conc.", line=dict(color='red')))
  fig.add_trace(go.Scatter(x = ['2020-03-01', '2020-04-15', '2020-07-20', '2020-11-15', '2021-01-20', '2021-03-27', '2021-06-15'], y = [800, 800, 800, 800, 800, 800, 800], 
                           mode="text", name="Labels", text=["No Lockdown", "1st Lockdown", "No Lockdown", "2nd Lockdown", "No Lockdown", "3rd Lockdown", "No Lockdown"], textposition="top center"))
  fig.update_xaxes(title_text = "Date", rangeslider_visible=True, showline=True, linewidth=2, linecolor='black', mirror=True)
  fig.update_yaxes(title_text = "Average Concentration", showline=True, linewidth=2, linecolor='black', mirror=True)
  fig.update_layout(height=700, width=1500, title_text="Average Concentration (Unit - µg/m³) of Air Pollutants in France from 2020-21 :: " + city,
                      shapes = [dict(type = "rect", y0 = -50, y1 = 1000, x0="2020-02-05", x1="2020-03-17", name = "No Lockdown", fillcolor = "green", opacity = 0.5),
                                dict(type = "rect", y0 = -50, y1 = 1000, x0="2020-03-17", x1="2020-05-10", name = "1st Lockdown", fillcolor = "red", opacity = 0.5),
                                dict(type = "rect", y0 = -50, y1 = 1000, x0="2020-05-10", x1="2020-10-17", name = "No Lockdown", fillcolor = "green", opacity = 0.5), 
                                dict(type = "rect", y0 = -50, y1 = 1000, x0="2020-10-17", x1="2020-12-14", name = "2nd Lockdown", fillcolor = "red", opacity = 0.5),
                                dict(type = "rect", y0 = -50, y1 = 1000, x0="2020-12-14", x1="2021-02-26", name = "No Lockdown", fillcolor = "green", opacity = 0.5),
                                dict(type = "rect", y0 = -50, y1 = 1000, x0="2021-02-26", x1="2021-05-02", name = "3rd Lockdown", fillcolor = "red", opacity = 0.5),
                                dict(type = "rect", y0 = -50, y1 = 1000, x0="2021-05-02", x1="2021-07-27", name = "No Lockdown", fillcolor = "green", opacity = 0.5)]) 
  #fig.show()
  st.plotly_chart(fig)  
  

max = data[["date", "City", "('max', 'co')", "('max', 'dew')", "('max', 'humidity')",
       "('max', 'no2')", "('max', 'o3')", "('max', 'pm10')",
       "('max', 'pm25')", "('max', 'pressure')", "('max', 'so2')",
       "('max', 'temperature')", "('max', 'wind gust')",
       "('max', 'wind speed')"]]

max = max[["date", "City", "('max', 'co')", "('max', 'dew')", "('max', 'no2')", "('max', 'o3')", "('max', 'pm10')", "('max', 'pm25')", "('max', 'so2')"]]
max = max.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
max.sort_values(["date", "Pollutants"], inplace = True)

min = data[["date", "City", "('min', 'co')", "('min', 'dew')", "('min', 'humidity')", 
       "('min', 'no2')", "('min', 'o3')", "('min', 'pm10')",
       "('min', 'pm25')", "('min', 'pressure')", "('min', 'so2')",
       "('min', 'temperature')", "('min', 'wind gust')",
       "('min', 'wind speed')"]]

min = min[["date", "City", "('min', 'co')", "('min', 'dew')", "('min', 'no2')", "('min', 'o3')", "('min', 'pm10')", "('min', 'pm25')", "('min', 'so2')"]]
min = min.melt(id_vars=["date", "City"], var_name = "Pollutants", value_name = "Concentration")
min.sort_values(["date", "Pollutants"], inplace = True)

st.header("PART 3")

st.subheader("Visualization All Lockdown Phases - Region Wise")


if st.checkbox("Plot Bordeaux"): 
        plot("Bordeaux")

if st.checkbox("Plot Grenoble"): 
        plot("Grenoble")

if st.checkbox("Plot Lille"): 
        plot("Lille")

if st.checkbox("Plot Lyon"): 
        plot("Lyon")

if st.checkbox("Plot Marseille"): 
        plot("Marseille")

if st.checkbox("Plot Montepellier"): 
        plot("Montpellier")

if st.checkbox("Plot Nantes"): 
        plot("Nantes")

if st.checkbox("Plot Nice"): 
        plot("Nice")

if st.checkbox("Plot Paris"): 
        plot("Paris")

if st.checkbox("Plot Rouen"): 
        plot("Rouen")

if st.checkbox("Plot Strasbourg"): 
        plot("Strasbourg")

if st.checkbox("Plot Toulouse"): 
        plot("Toulouse")

