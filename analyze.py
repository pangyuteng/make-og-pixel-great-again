import datetime
import pandas as pd
import numpy as np

df = pd.read_csv('all.csv')
df['tstamp']=df.creationTime.apply(
    lambda x: datetime.datetime.strptime(x,'%Y-%m-%dT%H:%M:%SZ')
)
print(df.shape)
df = df[df.tstamp>datetime.datetime(2021,5,30,0,0,0)].reset_index()
print(df.shape)

for cameraModel in df.cameraModel.unique():
    if isinstance(cameraModel,str):
        tmpdf = df[df.cameraModel==cameraModel]
    else:
        tmpdf = df[df.cameraModel.isna()]
    print(cameraModel,len(tmpdf))
