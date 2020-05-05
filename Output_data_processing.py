# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 16:45:24 2019

@author: Silvia
"""


import pandas as pd
connections=pd.read_csv('connections_output.csv')
coordinates=pd.read_csv(r'C:\Users\Asus\Documents\GitHub\Gisele_MILP\Namanjavira.csv')
#voltages=pd.read_csv( 'Voltage.csv',names=['Voltage [p.u.]','id','PS','P in [MW]'])
#power=pd.read_csv('Power.csv',names=['Power [MW]'])

#create dataframe with voltage level of each node. Nodes are already ordered
#voltages['X']=coordinates['X']
#voltages['Y']=coordinates['Y']
#create dataframe with connections: to show the lines the point layer must loaded two times in qgis and use join by lines
connections['X1']=connections['id1']
connections['Y1']=connections['id1']
connections['X2']=connections['id1']
connections['Y2']=connections['id1']
#connections['Power [MW]']=power
'''
for i, row in connections.iterrows():
    connections.iloc[i,connections.columns.get_loc('X1')]=coordinates[coordinates['id']==row['id1']]['X'].values[0]
    connections.iloc[i,connections.columns.get_loc('Y1')]=coordinates[coordinates['id']==row['id1']]['Y'].values[0]
    connections.iloc[i,connections.columns.get_loc('X2')]=coordinates[coordinates['id']==row['id2']]['X'].values[0]
    connections.iloc[i,connections.columns.get_loc('Y2')]=coordinates[coordinates['id']==row['id2']]['Y'].values[0]
 '''

for i, row in connections.iterrows():
    connections.loc[i,'X1']=coordinates[coordinates['id']==row['id1']]['X'].values[0]
    connections.loc[i,'X2']=coordinates[coordinates['id']==row['id2']]['X'].values[0]
    connections.loc[i,'Y1'] = coordinates[coordinates['id'] == row['id1']]['Y'].values[0]
    connections.loc[i, 'Y2'] = coordinates[coordinates['id'] == row['id2']]['Y'].values[0]
outpath='final.csv'
connections.to_csv(outpath)
#voltages.to_csv('Voltage_profile1.csv')