import os
from pandas.io.parsers import read_csv
import numpy as np

ROOT_PATH = os.path.expanduser('~')
DATA_PATH = os.path.join(ROOT_PATH, 'picture/car_logger')
canfile = os.path.join(DATA_PATH, 'canbus_output.csv')
canfile2 = os.path.join(DATA_PATH, 'canbus_output2.csv')
output = os.path.join(DATA_PATH, "combine2file.csv")

df = read_csv(canfile2)
print df.shape
print df.columns
print df.dtypes
print df.index
print df.values
print df.head()
time = df["Time"]
print type(df)
print type(time)
print time.shape
print time.index
print time.values
print time.name