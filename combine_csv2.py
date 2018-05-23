import os
import csv
from pandas.io.parsers import read_csv
import numpy as np

ROOT_PATH = os.path.expanduser('~')
DATA_PATH = os.path.join(ROOT_PATH, 'picture/car_logger')
canfile = os.path.join(DATA_PATH, 'canbus_output.csv')
imgfile = os.path.join(DATA_PATH, 'img_output.csv')
canfile2 = os.path.join(DATA_PATH, 'canbus_output2.csv')
imgfile2 = os.path.join(DATA_PATH, 'img_output2.csv')
output = os.path.join(DATA_PATH, "combine2file.csv")

df = read_csv(canfile2)
print df.shape
print df.columns
print df.dtypes
print df.index
print df.values
time = df["Time"]
print type(df)
print type(time)
print time.shape
print time.index
print time.values
print time.name

# with open(canfile, 'rb') as input:
#     reader = csv.reader(input)
#     next(reader, None)  # skip the CSV header
#     canbus_data = [row for row in reader]
#     for i in range(len(canbus_data)):
#         canbus_data[i][0] = float(canbus_data[i][0].split('152687')[-1])
#         canbus_data[i][1] = int(canbus_data[i][1])
#         canbus_data[i][4] = int(canbus_data[i][4])
#
# with open(canfile2, 'wb') as outputfile:
#     csvwriter = csv.writer(outputfile)
#     csvwriter.writerow(['Time', 'Bus', 'MessageID', 'Message', 'MessageLength'])
#     for i in range(len(canbus_data)):
#         csvwriter.writerow(canbus_data[i])

# with open(imgfile, 'rb') as input:
#     reader = csv.reader(input)
#     next(reader, None)  # skip the CSV header
#     images_data = [row for row in reader]
#     for i in range(len(images_data)):
#         images_data[i][0] = float(images_data[i][0].split('152687')[-1])
#
#
# with open(imgfile2, 'wb') as outputfile:
#     csvwriter = csv.writer(outputfile)
#     csvwriter.writerow(['Time', 'Image name'])
#     for i in range(len(images_data)):
#         csvwriter.writerow(images_data[i])


# sec_since_boot = canbus_data[0][0]

print 0