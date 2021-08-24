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

st.subheader("COVID-19 Data")

"Loading the COVID-19 Data...."

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
