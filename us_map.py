# https://www.kaggle.com/abigaillarion/terrorist-attacks-in-united-states

import pandas as pd
from plotly.offline import plot

pd.options.mode.chained_assignment = None

columns_to_use = [0, 1, 2, 3, 8, 11, 13, 14, 35, 82, 98, 101]
terror_data = pd.read_csv('./input/globalterrorismdb_0617dist.csv', encoding='ISO-8859-1',
                          usecols=columns_to_use)
terror_data = terror_data.rename(
    columns={'eventid': 'id', 'iyear': 'year', 'imonth': 'month', 'iday': 'day',
             'country_txt': 'country', 'provstate': 'state', 'targtype1_txt': 'target',
             'weaptype1_txt': 'weapon', 'nkill': 'fatalities', 'nwound': 'injuries'})

terror_data['fatalities'] = terror_data['fatalities'].fillna(0).astype(int)
terror_data['injuries'] = terror_data['injuries'].fillna(0).astype(int)

# terrorist attacks in United States only (2,198 rows)
terror_usa = terror_data[(terror_data.country == 'United States') & (terror_data.state != 'Puerto Rico') &
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

fatality_marker = dict(size=terror_usa[terror_usa.fatalities > 0]['fatalities'] ** 0.255 * 8, opacity=0.95,
                       color='rgb(240, 140, 45)')
fatality = dict(
    hoverinfo='text+name', lat=terror_usa[terror_usa.fatalities > 0]['latitude'],
    locationmode='USA-states', lon=terror_usa[terror_usa.fatalities > 0]['longitude'],
    mode='markers', marker=fatality_marker, name='Fatalities',
    text=terror_usa[terror_usa.fatalities > 0]['text'], type='scattergeo'
)

injury_marker = dict(size=(terror_usa[terror_usa.fatalities == 0]['injuries'] + 1) ** 0.245 * 8, opacity=0.85,
                     color='rgb(20, 150, 187)')
injury = dict(
    hoverinfo='text+name', lat=terror_usa[terror_usa.fatalities == 0]['latitude'],
    locationmode='USA-states', lon=terror_usa[terror_usa.fatalities == 0]['longitude'],
    mode='markers', name='Injuries', marker=injury_marker,
    text=terror_usa[terror_usa.fatalities == 0]['text'], type='scattergeo'
)

layout_legend = dict(x=0.85, y=0.4)
layout_geo = dict(scope='usa', projection=dict(type='albers usa'), showland=True, landcolor='rgb(250, 250, 250)',
                  subunitwidth=1,
                  subunitcolor='rgb(217, 217, 217)', countrywidth=1, countrycolor='rgb(217, 217, 217)', showlakes=True,
                  lakecolor='rgb(255, 255, 255)')
layout = dict(
    title='Terrorist Attacks by Latitude/Longitude in United States (1970-2015)',
    showlegend=True,
    legend=layout_legend,
    geo=layout_geo
)

data = [fatality, injury]
figure = dict(data=data, layout=layout)

plot(figure)
