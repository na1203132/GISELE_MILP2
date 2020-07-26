
import pandapower as pp
from pandapower.plotting import simple_plot, simple_plotly, pf_res_plotly
import pandas as pd
import matplotlib.pyplot as plt

net = pp.create_empty_network()

df= pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\gdf_clusters.csv")
main_intr= pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\total_maininter.csv")
coll_intr=pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\total_collinter.csv")
intrC= pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\total_interconnection.csv")
PS=pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\PS_withIndex.csv")
loads=pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\total_load.csv")


for i in loads.index:
  if loads.loc[i]['Population'] == 0:
        loads.drop(i,inplace=True)


df.index=df['ID']
loads.index=loads['ID']
PS.index=PS['i']

main_intr.index=main_intr['ID']
main_idx=main_intr['ID']
main_intr.index=main_intr['i']

coll_intr.index=coll_intr['ID']
coll_idx=coll_intr['ID']
coll_intr.index=coll_intr['i']

intrC.index=intrC['ID']
intrC_idx=intrC['ID']
intrC.index=intrC['i']

main_idx.drop_duplicates(inplace=True)
coll_idx.drop_duplicates(inplace=True)
intrC_idx.drop_duplicates(inplace=True)



##### CREATE MAIN BRANCH: BUSES & LINES ###############
# creating Secondary Substations
for i in main_idx.index:
     if(df.at[i,"Population"] == "0"):
        pp.create_bus(net, vn_kv=20, type='n', index=main_idx[i], geodata=(df.at[main_idx[i], "X"], df.at[main_idx[i], "Y"]))
     else:
        pp.create_bus(net, vn_kv=20, type='b', index=main_idx[i], geodata=(df.at[main_idx[i], "X"], df.at[main_idx[i], "Y"]))

for i in main_intr.index:
     pp.create_line(net, from_bus=main_intr.at[i, 'ID1'], to_bus=main_intr.at[i, 'ID2'], length_km=1, std_type="NA2XS2Y 1x240 RM/25 12/20 kV")



##### CREATE COLLATERAL BRANCH: BUSES & LINES ###############
for i in coll_idx.index:
       if(coll_idx[i] in main_idx.index):
           coll_idx.drop(index=i, inplace=True)

for i in coll_idx.index:
         if(df.at[i,"Population"] == "0"):
            pp.create_bus(net, vn_kv=20, type='n', index=coll_idx[i], geodata=(df.at[coll_idx[i], "X"], df.at[coll_idx[i], "Y"]))
         else:
            pp.create_bus(net, vn_kv=20, type='b', index=coll_idx[i], geodata=(df.at[coll_idx[i], "X"], df.at[coll_idx[i], "Y"]))

### One Node is missing from the DataFrame obtained from QGIS, it is added here manually
pp.create_bus(net, vn_kv=20, type='n', index=2020, geodata=(df.at[2020, "X"], df.at[2020, "Y"]))

for i in coll_intr.index:
     pp.create_line(net, from_bus=coll_intr.at[i, 'ID1'], to_bus=coll_intr.at[i, 'ID2'], length_km=1, std_type="NAYY 4x50 SE")


##### CREATE INTERCONNECTION BETWEEN CLUSTERS: BUSES & LINES ###############
# creating Secondary Substations
for i in intrC_idx.index:
       if((intrC_idx[i] in main_idx.index) or (intrC_idx[i] in coll_idx.index)):
           intrC_idx.drop(index=i, inplace=True)

for i in intrC_idx.index:
     if(df.at[i,"Population"] == "0"):
        pp.create_bus(net, vn_kv=20, type='n', index=intrC_idx[i], geodata=(df.at[intrC_idx[i], "X"], df.at[intrC_idx[i], "Y"]))
     else:
        pp.create_bus(net, vn_kv=20, type='b', index=intrC_idx[i], geodata=(df.at[intrC_idx[i], "X"], df.at[intrC_idx[i], "Y"]))

for i in intrC.index:
     pp.create_line(net, from_bus=intrC.at[i, 'ID1'], to_bus=intrC.at[i, 'ID2'], length_km=1, std_type="NA2XS2Y 1x240 RM/25 12/20 kV")





##############################################
#Creating Load
for i in loads.index:
    pp.create_load(net, loads.at[i,'ID'], p_mw=0.1)

##############################################
#creating External Grid (Slack Bus)
for i in PS.index:
    pp.create_bus(net, vn_kv=110, type='b', index=i, geodata=(PS.at[i, "X"], PS.at[i, "Y"]))
    pp.create_ext_grid(net, i, vm_pu = 1)
    if(i==3):
        pp.create_transformer(net, hv_bus=i, lv_bus=PS.at[i,'ID'],tap_pos="4",std_type="25 MVA 110/20 kV")
    else:
        pp.create_transformer(net, hv_bus=i, lv_bus=PS.at[i, 'ID'],tap_pos="1", std_type="25 MVA 110/20 kV")

pp.runpp(net)
print(net.res_bus)
pp.plotting.plot_voltage_profile(net)
pf_res_plotly(net,bus_size=10)
plt.show()