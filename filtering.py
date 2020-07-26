import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix
from scipy.spatial import KDTree

df=pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\Mcluster.csv")
df.index=df["id"]

df1=pd.DataFrame()
coords1=pd.DataFrame()


for i in df.index:
  if (df.at[i,'Population'] > 30) and (df.at[i,'M'] == 1):
       coords1.at[i,'X']= df.at[i,'X']
       coords1.at[i,'Y']= df.at[i,'Y']
       idx= coords1.index


coords=pd.DataFrame()
coords['X']=df['X']
coords['Y']=df['Y']


Dist_matrix=pd.DataFrame(distance_matrix(coords.values, coords.values), index=df['id'], columns=df['id'])


min=Dist_matrix[Dist_matrix > 0].idxmin(axis=1)


for i in coords1.index:
    df1.at[i, 'X'] = df.at[min[i], 'X']
    df1.at[i, 'Y'] = df.at[min[i], 'Y']
    df1.at[i, 'Weight'] = df.at[min[i], 'Weight']
    df1.at[i, 'Population'] = df.at[min[i], 'Population']

df1.to_csv('filtered.csv',index=False)




