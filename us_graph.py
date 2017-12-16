# https://www.kaggle.com/abigaillarion/terrorist-attacks-in-united-states

import numpy as np
import pandas as pd
import plotly.graph_objs as graph_objs
from plotly.offline import plot
pd.options.mode.chained_assignment = None

terror_data = pd.read_csv('./input/globalterrorismdb_0617dist.csv', encoding='ISO-8859-1',
                          usecols=[0, 1, 2, 3, 8, 11, 13, 14, 35, 82, 98, 101])
terror_data = terror_data.rename(
    columns={'eventid': 'id', 'iyear': 'year', 'imonth': 'month', 'iday': 'day',
             'country_txt': 'country', 'provstate': 'state', 'targtype1_txt': 'target',
             'weaptype1_txt': 'weapon', 'nkill': 'fatalities', 'nwound': 'injuries'})

terror_data['fatalities'] = terror_data['fatalities'].fillna(0).astype(int)
terror_data['injuries'] = terror_data['injuries'].fillna(0).astype(int)

# terrorist attacks in United States only (2,198 rows)
terror_usa = terror_data[(terror_data.country == 'United States') &
                         (terror_data.state != 'Puerto Rico') &
                         (terror_data.longitude < 0)]
terror_usa['day'][terror_usa.day == 0] = 1
terror_usa['date'] = pd.to_datetime(terror_usa[['day', 'month', 'year']])
terror_usa = terror_usa[['id', 'date', 'year', 'state', 'latitude', 'longitude',
                         'target', 'weapon', 'fatalities', 'injuries']]
terror_usa = terror_usa.sort_values(['fatalities', 'injuries'], ascending=False)
terror_usa = terror_usa.drop_duplicates(['date', 'latitude', 'longitude', 'fatalities'])

terror_usa['text'] = terror_usa['date'].dt.strftime('%B %-d, %Y') + '<br>' + \
                     terror_usa['fatalities'].astype(str) + ' Killed, ' + \
                     terror_usa['injuries'].astype(str) + ' Injured'

fatality = dict(
    type='scattergeo',
    locationmode='USA-states',
    lon=terror_usa[terror_usa.fatalities > 0]['longitude'],
    lat=terror_usa[terror_usa.fatalities > 0]['latitude'],
    text=terror_usa[terror_usa.fatalities > 0]['text'],
    mode='markers',
    name='Fatalities',
    hoverinfo='text+name',
    marker=dict(
        size=terror_usa[terror_usa.fatalities > 0]['fatalities'] ** 0.255 * 8,
        opacity=0.95,
        color='rgb(240, 140, 45)')
)

injury = dict(
    type='scattergeo',
    locationmode='USA-states',
    lon=terror_usa[terror_usa.fatalities == 0]['longitude'],
    lat=terror_usa[terror_usa.fatalities == 0]['latitude'],
    text=terror_usa[terror_usa.fatalities == 0]['text'],
    mode='markers',
    name='Injuries',
    hoverinfo='text+name',
    marker=dict(
        size=(terror_usa[terror_usa.fatalities == 0]['injuries'] + 1) ** 0.245 * 8,
        opacity=0.85,
        color='rgb(20, 150, 187)')
)

layout = dict(
    title='Terrorist Attacks by Latitude/Longitude in United States (1970-2015)',
    showlegend=True,
    legend=dict(
        x=0.85, y=0.4
    ),
    geo=dict(
        scope='usa',
        projection=dict(type='albers usa'),
        showland=True,
        landcolor='rgb(250, 250, 250)',
        subunitwidth=1,
        subunitcolor='rgb(217, 217, 217)',
        countrywidth=1,
        countrycolor='rgb(217, 217, 217)',
        showlakes=True,
        lakecolor='rgb(255, 255, 255)')
)

data = [fatality, injury]
figure = dict(data=data, layout=layout)

plot(figure)

# terrorist attacks by year
terror_peryear = np.asarray(terror_usa.groupby('year').year.count())

terror_years = np.arange(1970, 2016)
# terrorist attacks in 1993 missing from database
terror_years = np.delete(terror_years, [23])

trace = [graph_objs.Scatter(
    x=terror_years,
    y=terror_peryear,
    mode='lines',
    line=dict(
        color='rgb(240, 140, 45)',
        width=3)
)]

layout = graph_objs.Layout(
    title='Terrorist Attacks by Year in United States (1970-2015)',
    xaxis=dict(
        rangeslider=dict(thickness=0.05),
        showline=True,
        showgrid=False
    ),
    yaxis=dict(
        range=[0.1, 425],
        showline=True,
        showgrid=False)
)

figure = dict(data=trace, layout=layout)
# plot(figure)
