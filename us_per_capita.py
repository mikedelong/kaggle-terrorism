# https://www.kaggle.com/abigaillarion/terrorist-attacks-in-united-states

import numpy as np
import pandas as pd
from plotly.offline import plot

us_states = np.asarray(['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA',
                        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',
                        'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                        'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                        'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'])

# state population estimates for July 2015 from US Census Bureau
state_population = np.asarray([4858979, 738432, 6828065, 2978204, 39144818, 5456574,
                               3590886, 945934, 646449, 20271272, 10214860, 1431603,
                               1654930, 12859995, 6619680, 3123899, 2911641, 4425092,
                               4670724, 1329328, 6006401, 6794422, 9922576, 5489594,
                               2992333, 6083672, 1032949, 1896190, 2890845, 1330608,
                               8958013, 2085109, 19795791, 10042802, 756927, 11613423,
                               3911338, 4028977, 12802503, 1056298, 4896146, 858469,
                               6600299, 27469114, 2995919, 626042, 8382993, 7170351,
                               1844128, 5771337, 586107])

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

# terrorist attacks per 100,000 people in state
terror_perstate = np.asarray(terror_usa.groupby('state').state.count())
terror_percapita = np.round(terror_perstate / state_population * 100000, 2)
# District of Columbia outlier (1 terrorist attack per 10,000 people) adjusted
terror_percapita[8] = round(terror_percapita[8] / 6, 2)

terror_scale = [[0, 'rgb(252, 232, 213)'], [1, 'rgb(240, 140, 45)']]

marker_line = dict(color='rgb(255, 255, 255)', width=2)
data = [dict(autocolorscale=False, colorscale=terror_scale, locationmode='USA-states',
             locations=us_states, showscale=False, type='choropleth', z=terror_percapita,
             marker=dict(line=marker_line))]

layout_projection = dict(type='albers usa')
layout_geo = dict(countrycolor='rgb(255, 255, 255)', lakecolor='rgb(255, 255, 255)')
layout = dict(title='Terrorist Attacks per 100,000 People in United States (1970-2015)',
              geo=layout_geo, projection=layout_projection, scope='usa', showlakes=True)

figure = dict(data=data, layout=layout)
plot(figure)
