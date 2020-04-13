import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
import plotly.express as px
import plotly.graph_objects as go

#%matplotlib inline

import datetime as dt
from datetime import date
today = dt.date.today()
# yesterday = today - dt.timedelta(days=1)
#%%

##################################################################

googleSheetId = '16g_PUxKYMC0XjeEKF6FPUBq2-pFgmTkHoj5lbVrGLhE'
worksheetName1 = 'Historical'
worksheetName2 = 'Cases'
URL1 = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
    googleSheetId,
    worksheetName1
)

URL2 = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
    googleSheetId,
    worksheetName2
)
##################################################################




covid19_PH = pd.read_csv(URL1, encoding='utf-8')
covid19_PH_detailed = pd.read_csv(URL2, encoding='utf-8')

covid19_PH['Date'] = pd.to_datetime(covid19_PH['Date']).dt.date
covid19_PH['Admitted'] = covid19_PH['Cases'] - (covid19_PH['Deaths']+covid19_PH['Recoveries'])
#covid19_PH.tail()



#covid19_PH_detailed.head()



#covid19_PH_detailed.columns

#%%
covid19_PH_detailed['Date Announced'] = pd.to_datetime(covid19_PH_detailed['Date of Announcement to the Public']).dt.date
covid19_PH_detailed = covid19_PH_detailed.reindex(columns=['Case No.',
                        'Sex',
                        'Age',
                        'Nationality',
                        'Travel History',
                        'Epi Link',
                        'Admission / Consultation',
                        'Other disease',
                        'Date Announced',
                        'Date of Final Status (recovered/expired)',
                        'Date of Admission',
                        'Status',
                        'Final Diagnosis',
                        'Location',
                        'Latitude',
                        'Longitude',
                        'Residence in the Philippines',
                        'Residence Lat',
                        'Residence Long'])

covid19_PH_detailed['Residence Lat'] = pd.to_numeric(covid19_PH_detailed['Residence Lat'])
covid19_PH_detailed['Residence Long'] = pd.to_numeric(covid19_PH_detailed['Residence Long'])
covid19_PH_detailed['Latitude'] = pd.to_numeric(covid19_PH_detailed['Latitude'])
covid19_PH_detailed['Longitude'] = pd.to_numeric(covid19_PH_detailed['Longitude'])

covid19_PH_detailed.loc[covid19_PH_detailed['Status'] == 'Expired', 'Status'] = 'Dead'


covid19_PH_confirmed = covid19_PH_detailed.loc[:, ['Residence Lat',
                                                   'Residence Long']]

covid19_PH_confirmed = covid19_PH_confirmed.rename(columns={'Residence Lat': 'lat', 'Residence Long': 'lon'})

#covid19_PH_confirmed.head()

#%%

covid19_PH_recovered = covid19_PH_detailed.loc[covid19_PH_detailed['Status'] == 'Recovered', ['Residence Lat',
                                                                                              'Residence Long']]

covid19_PH_recovered = covid19_PH_recovered.rename(columns={'Residence Lat': 'lat', 'Residence Long': 'lon'})
#covid19_PH_recovered.head()

#%%

covid19_PH_died = covid19_PH_detailed.loc[covid19_PH_detailed['Status'] == 'Dead', ['Residence Lat',
                                                                                    'Residence Long']]

covid19_PH_died = covid19_PH_died.rename(columns={'Residence Lat': 'lat', 'Residence Long': 'lon'})
#covid19_PH_died.head()

#%%
covid19_PH_admitted = covid19_PH_detailed.loc[covid19_PH_detailed['Status'] == 'Admitted', ['Latitude',
                                                                                            'Longitude']]

covid19_PH_admitted = covid19_PH_admitted.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})
#covid19_PH_admitted.head()


age_PH = covid19_PH_detailed['Age'].value_counts()
age_PH = pd.DataFrame(age_PH).reset_index().sort_values(by=['index'])

age_PH = age_PH.rename(columns={'index': 'Age',
                         'Age': 'Count'})


place_PH = covid19_PH_detailed.reset_index()
place_PH = place_PH['Residence in the Philippines'].value_counts()
place_PH = pd.DataFrame(place_PH).reset_index()

place_PH = place_PH.rename(columns={'index': 'Hometown', 'Residence in the Philippines': 'Count'})

place_PH_valid = place_PH[place_PH['Hometown'] != 'For validation']


#%%

gender_PH = covid19_PH_detailed.reset_index()
gender_PH = covid19_PH_detailed['Sex'].value_counts()
gender_PH = pd.DataFrame(gender_PH).reset_index()

gender_PH = gender_PH.rename(columns={'index': 'Sex',
                         'Sex': 'count'})

gender_PH.loc[gender_PH['Sex'] == 'M', ['Sex']] = 'Male'
gender_PH.loc[gender_PH['Sex'] == 'F', ['Sex']] = 'Female'


#%%

hospitals_PH = covid19_PH_detailed.reset_index()
hospitals_PH = covid19_PH_detailed['Admission / Consultation'].value_counts()
hospitals_PH = pd.DataFrame(hospitals_PH).reset_index()

hospitals_PH = hospitals_PH.rename(columns={'index': 'Hospital',
                         'Admission / Consultation': 'Patients Admitted'})


##################################################################
# Create dashboard

st.sidebar.title('Mga Kaso ng COVID-19 sa Pilipinas')
subtitle = "Huling datos: {}".format(today)
st.sidebar.markdown(subtitle)

confirmed_today = int(covid19_PH['Daily Case Increase'].sum())
died_today = int(covid19_PH['Daily Death'].sum())
recovered_today = int(covid19_PH['Daily Recovery'].sum())
admitted_today = int(confirmed_today-died_today-recovered_today)
tested_today = int(covid19_PH['Tests Conducted'].sum())


daily_fig = covid19_PH.loc[:, ['Date', 'Daily Case Increase', 'Daily Death', 'Daily Recovery']]
daily_fig = daily_fig.dropna()
cumulative_fig = covid19_PH.loc[:, ['Date', 'Cases', 'Admitted', 'Deaths', 'Recoveries']]
cumulative_fig = cumulative_fig.dropna()




st.sidebar.markdown(
"""
<span style="color: red; box-sizing: content-box; display: table;
  width: 100%;
  padding: 18px;
  overflow: hidden;
  border: none;
  font: normal normal bold 18px/1 Arial;
  color: rgba(255,255,255,1);
  text-align: left;
  background: royalblue; ">Bilang ng Positibo: {}</span>
""".format(confirmed_today), unsafe_allow_html=True)

st.sidebar.markdown(
"""
<span style="color: red; box-sizing: content-box; display: table;
  width: 100%;
  padding: 18px;
  overflow: hidden;
  border: none;
  font: normal normal bold 18px/1 Arial;
  color: rgba(255,255,255,1);
  text-align: left;
  background: purple; ">Bilang ng May-Sakit Pa: {}</span>
""".format(admitted_today), unsafe_allow_html=True)


st.sidebar.markdown(
"""
<span style="color: red; box-sizing: content-box; display: table;
  width: 100%;
  padding: 18px;
  overflow: hidden;
  border: none;
  font: normal normal bold 18px/1 Arial;
  color: rgba(255,255,255,1);
  text-align: left;
  background: black; ">Bilang ng Namatay: {}</span>
""".format(died_today), unsafe_allow_html=True)

st.sidebar.markdown(
"""
<span style="color: red; box-sizing: content-box; display: table;
  width: 100%;
  padding: 18px;
  overflow: hidden;
  border: none;
  font: normal normal bold 18px/1 Arial;
  color: rgba(255,255,255,1);
  text-align: left;
  background: green; ">Bilang ng Gumaling: {}</span>
""".format(recovered_today), unsafe_allow_html=True)

st.sidebar.markdown(
"""
<span style="color: red; box-sizing: content-box; display: table;
  width: 100%;
  padding: 18px;
  overflow: hidden;
  border: none;
  font: normal normal bold 18px/1 Arial;
  color: rgba(255,255,255,1);
  text-align: left;
  background: maroon; ">Bilang ng Na-test: {}</span>
""".format(tested_today), unsafe_allow_html=True)

st.sidebar.markdown("-------------------------------")
st.sidebar.markdown("### Bilang ng mga Taong may Covid-19 kada Ospital")
st.sidebar.table(hospitals_PH)



##################################################
# map of cases
st.markdown("""
<span style="color: red; box-sizing: content-box; display: table;
  width: 100%;
  padding: 18px;
  overflow: hidden;
  border: none;
  font: normal normal bold 30px/1 Verdana;
  color: white;
  text-align: center;
  background: #00566e; "> MGA DATOS AT IMPORMASYON TUNGKOL SA COVID-19 SA PILIPINAS</span>
""", unsafe_allow_html=True)


st.markdown("-------------------------------")

map_confirmed = px.scatter_mapbox(covid19_PH_confirmed, lat='lat', lon='lon', zoom=4, width=800, height=600,
                                  title= "Mapa ng mga Kumpirmadong Kaso ng COVID-19")
map_confirmed.update_layout(mapbox_style="stamen-toner", title_font_size=24)
map_confirmed.update_traces(marker=dict(color='darkorange'))

map_admit = px.scatter_mapbox(covid19_PH_admitted, lat='lat', lon='lon', zoom=4, width=800, height=600,
                              title= "Mapa ng mga Naka-admit Dahil sa COVID-19")
map_admit.update_layout(mapbox_style="stamen-toner", title_font_size=24)

map_dead = px.scatter_mapbox(covid19_PH_died, lat='lat', lon='lon', zoom=4, width=800, height=600,
                             title= "Mapa ng mga Namatay sa COVID-19")
map_dead.update_layout(mapbox_style="stamen-toner", title_font_size=24)
map_dead.update_traces(marker=dict(color='red'))

map_recovered = px.scatter_mapbox(covid19_PH_recovered, lat='lat', lon='lon', zoom=4, width=800, height=600,
                             title= "Mapa ng mga Gumaling sa COVID-19")
map_recovered.update_layout(mapbox_style="stamen-toner", title_font_size=24)
map_recovered.update_traces(marker=dict(color='darkgreen'))

maps = {'Mga Kumpirmadong Kaso': map_confirmed,
        'Mga Naka-admit': map_admit,
        'Mga Namatay': map_dead,
        'Mga Gumaling': map_recovered}
saan = st.selectbox("Lokasyon ng mga Kasalakuyang Kaso ng COVID-19", list(maps.keys()), 0)
st.plotly_chart(maps[saan], use_column_width=True, caption=maps[saan])



# plot of confirmed cases
daily_confirmed= go.Figure()
daily_confirmed.add_trace(go.Scatter(x=daily_fig['Date'], y=daily_fig['Daily Case Increase'],
                                     line=dict(color='blue', width=1)))
daily_confirmed.add_trace(go.Bar(x=daily_fig['Date'], y=daily_fig['Daily Case Increase'],
                                 marker=dict(color='dodgerblue', opacity=0.4)))
daily_confirmed.update_layout(showlegend=False, xaxis_title="Petsa", yaxis_title="Dami ng Tao",
                              title= "Graph ng mga Kumpirmadong Kaso ng COVID-19",
                              title_font_size=24)

#st.plotly_chart(daily_confirmed, use_container_width=True)


# plot of deaths
daily_deaths = go.Figure()
daily_deaths.add_trace(go.Scatter(x=daily_fig['Date'], y=daily_fig['Daily Death'],
                                     line=dict(color='darkred', width=1)))
daily_deaths.add_trace(go.Bar(x=daily_fig['Date'], y=daily_fig['Daily Death'],
                                 marker=dict(color='red', opacity=0.4)))
daily_deaths.update_layout(showlegend=False, xaxis_title="Petsa", yaxis_title="Dami ng Tao",
                           title= "Graph ng mga Namatay sa COVID-19",
                           title_font_size=24)

#st.plotly_chart(daily_deaths, use_container_width=True)


# plot of recoveries
daily_recoveries = go.Figure()
daily_recoveries.add_trace(go.Scatter(x=daily_fig['Date'], y=daily_fig['Daily Recovery'],
                                     line=dict(color='darkgreen', width=1)))
daily_recoveries.add_trace(go.Bar(x=daily_fig['Date'], y=daily_fig['Daily Recovery'],
                                 marker=dict(color='green', opacity=0.4)))
daily_recoveries.update_layout(showlegend=False, xaxis_title="Petsa", yaxis_title="Dami ng Tao",
                               title= "Graph ng mga Gumaling sa COVID-19",
                               title_font_size=24)

#st.plotly_chart(daily_recoveries, use_container_width=True)

graphs = {'Mga Kumpirmadong Kaso': daily_confirmed,
        'Mga Namatay': daily_deaths,
        'Mga Gumaling': daily_recoveries}
graph = st.selectbox("Graph ng mga Kasalakuyang Kaso ng COVID-19", list(graphs.keys()), 0)
st.plotly_chart(graphs[graph], use_column_width=True, caption=graphs[graph])


# stacked bar graph cumulative cases

### linear
cumulative_case = go.Figure(data=[
    go.Bar(name='Bilang ng Gumaling sa COVID-19', x=cumulative_fig['Date'], y=cumulative_fig['Recoveries'],
           marker=dict(color='green', opacity=0.5)),
    go.Scatter(x=cumulative_fig['Date'], y=cumulative_fig['Recoveries'], showlegend=False, fill='none',
                                     line=dict(color='darkgreen', width=1), stackgroup='one'),
    go.Bar(name='Bilang ng Namatay sa COVID-19', x=cumulative_fig['Date'], y=cumulative_fig['Deaths'],
           marker=dict(color='red', opacity=0.5)),
    go.Scatter(x=cumulative_fig['Date'], y=cumulative_fig['Deaths'], showlegend=False, fill='none',
               line=dict(color='darkred', width=1), stackgroup='one'),
    go.Bar(name='Bilang ng May COVID-19', x=cumulative_fig['Date'], y=cumulative_fig['Admitted'],
           marker=dict(color='dodgerblue', opacity=0.5)),
    go.Scatter(x=cumulative_fig['Date'], y=cumulative_fig['Admitted'], showlegend=False, fill='none',
               line=dict(color='blue', width=1), stackgroup='one')])

cumulative_case.update_layout(barmode='stack' , xaxis_title= "Petsa", yaxis_title= "Dami ng Tao",
                              title= "Graph ng Lahat ng mga Naitalang Kaso ng COVID-19",
                              title_font_size=24, legend=dict(x=0, y=0.9))


### logarithmic
ln_cumulative_case = go.Figure(data=[
    go.Bar(name='Bilang ng Gumaling sa COVID-19', x=cumulative_fig['Date'], y=np.log(cumulative_fig['Recoveries']),
           marker=dict(color='green', opacity=0.5)),
    go.Scatter(x=cumulative_fig['Date'], y=np.log(cumulative_fig['Recoveries']), showlegend=False, fill='none',
                                     line=dict(color='darkgreen', width=1), stackgroup='one'),
    go.Bar(name='Bilang ng Namatay sa COVID-19', x=cumulative_fig['Date'], y=np.log(cumulative_fig['Deaths']),
           marker=dict(color='red', opacity=0.5)),
    go.Scatter(x=cumulative_fig['Date'], y=np.log(cumulative_fig['Deaths']), showlegend=False, fill='none',
               line=dict(color='darkred', width=1), stackgroup='one'),
    go.Bar(name='Bilang ng May COVID-19', x=cumulative_fig['Date'], y=np.log(cumulative_fig['Admitted']),
           marker=dict(color='dodgerblue', opacity=0.5)),
    go.Scatter(x=cumulative_fig['Date'], y=np.log(cumulative_fig['Admitted']), showlegend=False, fill='none',
               line=dict(color='blue', width=1), stackgroup='one')])


ln_cumulative_case.update_layout(barmode='stack' , xaxis_title= "Petsa", yaxis_title= "Dami ng Tao (logarithmic)",
                              title= "Graph ng Lahat ng mga Naitalang Kaso ng COVID-19",
                              title_font_size=24, legend=dict(x=0, y=0.9))


graphs2 = {'Linear': cumulative_case,
          'Natural Logarithm': ln_cumulative_case
          }
graph2 = st.selectbox("Pumili ng Klase ng Graph (Linear o Logarithmic)", list(graphs2.keys()), 0)

st.plotly_chart(graphs2[graph2], use_column_width=True, caption=graphs2[graph2])


##################################################################
#COVID-19 Histogram (Age/Gender)

age_PH_hist = px.histogram(covid19_PH_detailed, x='Age', nbins=20, color='Sex', height=400, width=800)
age_PH_hist.update_layout( xaxis_title="Bilang ng mga Taong May Covid-19", yaxis_title="Edad ng Pasyente",
                               title= "Graph ng Edad at Kasarian ng mga may COVID-19 sa Pilipinas",
                               title_font_size=20)
st.plotly_chart(age_PH_hist, use_container_width=True)

##################################################################
# COVID-19 Cases per LGU

place_PH_bar = px.bar(place_PH_valid, y="Hometown", x="Count", color="Count", height=2500, width=800, orientation='h')
place_PH_bar.update_layout(showlegend=False, xaxis_title="Bilang ng mga Taong May Covid-19",
                           yaxis_title="Lugar sa Pilipinas",
                           title_font_size=20, yaxis=dict(autorange="reversed"))
st.plotly_chart(place_PH_bar)


