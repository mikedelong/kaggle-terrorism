# https://www.kaggle.com/ash316/terrorism-around-the-world/notebook

import base64
import codecs
import io
import logging
import time
import warnings
from subprocess import check_output

import folium
import folium.plugins
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.offline as py
import plotly.tools as tls
import seaborn as sns
from IPython.display import HTML, display
from matplotlib import animation, rc
from mpl_toolkits.basemap import Basemap
from scipy.misc import imread

start_time = time.time()
# set up logging
formatter = logging.Formatter('%(asctime)s : %(name)s :: %(levelname)s : %(message)s')
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
console_handler.setLevel(logging.DEBUG)
logger.debug('started')

plt.style.use('fivethirtyeight')

if False:
    logger.debug(check_output(["ls", "../input"]).decode("utf8"))

data_path = './input/'

terror = pd.read_csv(data_path + 'globalterrorismdb_0617dist.csv', encoding='ISO-8859-1')
terror.rename(
    columns={'iyear': 'Year', 'imonth': 'Month', 'iday': 'Day', 'country_txt': 'Country', 'region_txt': 'Region',
             'attacktype1_txt': 'AttackType', 'target1': 'Target', 'nkill': 'Killed', 'nwound': 'Wounded',
             'summary': 'Summary', 'gname': 'Group', 'targtype1_txt': 'Target_type', 'weaptype1_txt': 'Weapon_type',
             'motive': 'Motive'}, inplace=True)
terror = terror[
    ['Year', 'Month', 'Day', 'Country', 'Region', 'city', 'latitude', 'longitude', 'AttackType', 'Killed', 'Wounded',
     'Target', 'Summary', 'Group', 'Target_type', 'Weapon_type', 'Motive']]
terror['casualties'] = terror['Killed'] + terror['Wounded']

plt.subplots(figsize=(15, 6))
sns.countplot('Year', data=terror, palette='RdYlGn_r', edgecolor=sns.color_palette('dark', 7))
plt.xticks(rotation=90)
plt.title('Activity count by year')
plt.tight_layout()
output_filename = 'activities_by_year.png'
plt.savefig(output_filename)

plt.subplots(figsize=(15, 6))
sns.countplot('AttackType', data=terror, palette='inferno', order=terror['AttackType'].value_counts().index)
plt.xticks(rotation=45)
plt.title('Method of attack')
output_filename = 'method_of_attack.png'
plt.tight_layout()
plt.savefig(output_filename)

global_map = Basemap(projection='mill', llcrnrlat=-80, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180, lat_ts=20,
                     resolution='c', lat_0=True, lat_1=True)
lat_100 = list(terror[terror['casualties'] >= 75].latitude)
long_100 = list(terror[terror['casualties'] >= 75].longitude)
x_100, y_100 = global_map(long_100, lat_100)
global_map.plot(x_100, y_100, 'go', markersize=5, color='r')
lat_ = list(terror[terror['casualties'] < 75].latitude)
long_ = list(terror[terror['casualties'] < 75].longitude)
x_, y_ = global_map(long_, lat_)
global_map.plot(x_, y_, 'go', markersize=2, color='b', alpha=0.4)
global_map.drawcoastlines()
global_map.drawcountries()
global_map.fillcontinents(lake_color='aqua')
global_map.drawmapboundary(fill_color='aqua')
fig = plt.gcf()
fig.set_size_inches(10, 6)
plt.title('Global Terrorist Attacks')
plt.legend(loc='lower left', handles=[mpatches.Patch(color='b', label="< 75 casualties"),
                                      mpatches.Patch(color='red', label='> 75 casualties')])
output_filename = 'global_attack_map.png'
plt.tight_layout()
plt.savefig(output_filename)

elapsed_time = time.time() - start_time
logger.debug('elapsed time %d seconds', elapsed_time)
