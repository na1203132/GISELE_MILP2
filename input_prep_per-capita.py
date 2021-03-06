# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 12:09:03 2019

@author: Silvia
"""
import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix
from scipy.spatial import KDTree

df=pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\small1.csv")


# for i in df.index:
#   if (df.loc[i]['Population'] == 0) and (df.loc[i]['PS'] == 0):
#         df.drop(i,inplace=True)


coords=pd.DataFrame()
coords['X']=df['X']
coords['Y']=df['Y']


Dist_matrix=pd.DataFrame(distance_matrix(coords.values, coords.values), index=df['id'], columns=df['id'])
Weight=pd.DataFrame()
PS=pd.DataFrame()
df.index=df['id']
Weight=df['Weight']

k=0
#for i, row in df.iterrows():
 #   if df.loc[i,'Population'] > 10:
 #      df[i, 'Weight']= 0




 #create new column with absorbed power

df=df.assign(Power=0.1)
df['Power']=df['M'].apply(lambda x: '0' if x == 0 else '0.1')
# df['Power']=df['PS'].apply(lambda x: '0' if x == 1  else '0.1')
# df['Power']=df['Population'].apply(lambda x: '0.1' if x < 10  else '-0.1')
print("PS and Population assignment done!")


#save nodes index
df['id'].to_csv('nodes.csv',index=False)

for i, row in df.iterrows():
   if df.loc[i,'PS'] == "1":
      PS.loc[i,'id'] = df.loc[i,'id']

#df.loc['56','Power']=-0.7
df['Power'].to_csv('power.csv')
df['PS'].to_csv('PS.csv')
#Create dataframe to save allowed connections (evertything but diagonal elements)
connection=pd.DataFrame(columns=['id1','id2','distance'])


k=0
for i, row in Dist_matrix.iterrows():
    print("this is i ", i,"from ", Dist_matrix.size)
    for j, column in row.iteritems():
        if column !=0:
            if i<=j:
                connection.loc[k,'id1']=i
                connection.loc[k,'id2']=j
            else:
                connection.loc[k, 'id1'] = j
                connection.loc[k, 'id2'] = i
            connection.loc[k,'distance']=column * ((Weight[i]+Weight[j])/2)
            k=k+1

connection.drop_duplicates(inplace=True)















## Finding the nearest 8 neighbouring points
#tree= KDTree(coords)
#dist,ind=tree.query(coords[0:],k=9)
#new_ind=ind+1
#T=pd.DataFrame(new_ind)
#D=pd.DataFrame(dist)
#connection.drop(connection.index, inplace=True)

#k=0
#for i, row in T.iterrows():
#    for j in range(8):
#        connection.loc[k,'id1'] = T.loc[i, 0]
#        connection.loc[k,'id2']=T.loc[i,j+1]
#        connection.loc[k,'distance']=D.loc[i,j+1]
#        k=k+1
########################################################






for i in connection.index:
    print("last step: ", i)
    if connection.loc[i,'distance'] > 2000 * ((Weight[connection.loc[i,'id1']]+Weight[connection.loc[i,'id2']])/2):
        connection.drop(i,inplace=True)


connection[['id1','id2']].to_csv('links.csv',index=False)
connection.to_csv('distances.csv',index=False)

