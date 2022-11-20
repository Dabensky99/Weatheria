import requests
import streamlit as st
from datetime import date, time
import pandas as pd
import numpy as np
import json

api_key = "fdf12377c588b01b96a938ffa03dee5b"

st.set_page_config(
    page_title="Weatheria",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a Bug': 'https://gregoryreis.com',
        'About': '#Welcome to HCI'
    })

st.title('Weatheria')
st.header('Find The Weather in Your Area')

st.subheader('Personal Info')

name = st.text_input('Name (optional)')

st.subheader("Pinpoint Location")

country = st.selectbox('Which Country do you live in?', ['United States', 'Japan', 'England'])

if country == "United States":
    city_array = ["Miami", "Dallas", "Hialeah"]

if country == "Japan":
    city_array = ["Tokyo", "Kyoto", "Hiroshima"]

if country == "England":
    city_array = ["London", "Manchester", "Durham"]

query = st.selectbox('Which city do you live in?', city_array)
url = "https://api.openweathermap.org/data/2.5/weather?q=" + \
    query + "&appid=" + api_key
response = requests.get(url).json()

date_selected = st.date_input('Select Date')

if st.button('Submit'):
    st.success("Successfully retrieved weather data.")
    city_weather = response["weather"][0]["description"]
    city_temperature = response["main"]["temp"]
    city_temperature = "{:.1f}".format((city_temperature * 1.8) - 459.67)
    city_feeling = response["main"]["feels_like"]
    city_feeling = "{:.1f}".format((city_feeling * 1.8) - 459.67)
    st.write("Hello", name,", the weather on", date_selected, "in", query, " is {}".format(
        city_weather), "at {}".format(city_temperature), "degrees. However, it feels like {}".format(city_feeling), "degrees.")

st.subheader('Temperature Report')
days = 7

graph_type = st.radio('How would you like to view the report?', ['Bar Graph', 'Line Graph', 'Table'])

campuses_map = st.checkbox("View Map")
if campuses_map:
    st.write('User selected the field')
    map_data = pd.DataFrame(
        np.array([
            [response["coord"]["lat"], response["coord"]["lon"]],
        ]),
        columns=['lat', 'lon'])
    st.map(map_data)

sliders = st.checkbox("Adjust Days")
if sliders:
    st.info('Integer Slider for Report Days')
    days = st.slider('How many days would you like in the report?', 0, 31, 7)
    st.write("Days reported: ", str(days))

chart_data = pd.DataFrame(
        np.random.randn(days, 1) + (((response["main"]["temp"])* 1.8) - 459.67),
        columns=[query])

if graph_type == "Bar Graph":
    st.bar_chart(chart_data)

if graph_type == "Line Graph":
    st.line_chart(chart_data)

if graph_type == "Table":
    st.dataframe(chart_data)

