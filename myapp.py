import pandas as pd

from os.path import dirname, join
from script.covid import *
from bokeh.io import curdoc

# Membaca file csv
df = pd.read_csv(join(dirname(__file__), "data", "covid.csv"))

# Mengubah datatype untuk kolom date menjadi datetime
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
layout = covid(df)

# App configuration
curdoc().add_root(layout)
curdoc().theme = "dark_minimal"
curdoc().title = "Kasus COVID-19 Dunia"
