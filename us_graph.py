# https://www.kaggle.com/abigaillarion/terrorist-attacks-in-united-states

import numpy as np
import pandas as pd
import plotly.graph_objs as graph_objs
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

# terrorist attacks by year
terror_peryear = np.asarray(terror_usa.groupby('year').year.count())

terror_years = np.arange(1970, 2016)
# terrorist attacks in 1993 missing from database
terror_years = np.delete(terror_years, [23])

trace_line = dict(color='rgb(240, 140, 45)', width=3)
trace = [graph_objs.Scatter(line=trace_line, mode='lines', x=terror_years, y=terror_peryear)]

layout_xaxis = dict(rangeslider=dict(thickness=0.05), showline=True, showgrid=False)
layout_yaxis = dict(range=[0.1, 425], showline=True, showgrid=False)
layout = graph_objs.Layout(title='Terrorist Attacks by Year in United States (1970-2015)', xaxis=layout_xaxis,
                           yaxis=layout_yaxis)

figure = dict(data=trace, layout=layout)
plot(figure)
