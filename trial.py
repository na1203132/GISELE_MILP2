import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix
from scipy.spatial import KDTree

df=pd.read_csv(r"C:\Users\Asus\Desktop\POLIMI\Thesis\GISELE\New folder\Gisele_MILP-master\Cluster3.csv")


for i in df.index:
    if df.loc[i]['Population'] == 0:
         df.drop(i,inplace=True)

df.to_csv(r"C:\Users\Asus\Desktop\POLIMI\Thesis\GISELE\New folder\Gisele_MILP-master\Filtered_Cluster3.csv")
