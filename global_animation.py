# https://www.kaggle.com/ronaldtroncoso20/global-terrorism-trends-animation

import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
# import matplotlib.animation as animation
# from IPython.display import HTML
# import warnings
# warnings.filterwarnings('ignore')


input_file_name = './input/globalterrorismdb_0617dist.csv'
try:
    t_file = pd.read_csv(input_file_name, encoding='ISO-8859-1')
    print('File load: Success')
except:
    print('File load: Failed')