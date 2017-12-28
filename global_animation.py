# https://www.kaggle.com/ronaldtroncoso20/global-terrorism-trends-animation

import pandas as pd

# import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap

# import matplotlib.animation as animation
# from IPython.display import HTML
# import warnings
# warnings.filterwarnings('ignore')


input_file_name = './input/globalterrorismdb_0617dist.csv'
try:
    t_file = pd.read_csv(input_file_name, encoding='ISO-8859-1')
    print('File load: Success')
    regions = list(set(t_file.region_txt))
    colors = ['yellow', 'red', 'lightblue', 'purple', 'green', 'orange', 'brown', 'aqua', 'lightpink', 'lightsage',
              'lightgray', 'navy']
    plt.figure(figsize=(15, 8))
    m = Basemap(projection='mill', llcrnrlat=-80, urcrnrlat=80, llcrnrlon=-180, urcrnrlon=180, lat_ts=20,
                resolution='c')
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='burlywood', lake_color='lightblue', zorder=1)
    m.drawmapboundary(fill_color='lightblue')


    def pltpoints(region, color=None, label=None):
        x, y = m(list(t_file.longitude[t_file.region_txt == region].astype("float")),
                 (list(t_file.latitude[t_file.region_txt == region].astype("float"))))
        points = m.plot(x, y, "o", markersize=4, color=color, label=label, alpha=.5)
        return (points)


    for i, region in enumerate(regions):
        pltpoints(region, color=colors[i], label=region)

    plt.title("Global Terrorism (1970 - 2015)")
    plt.legend(loc='lower left', prop={'size': 11})
    plt.show()
except:
    print('File load: Failed')
