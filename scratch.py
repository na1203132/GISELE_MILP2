
import pandapower as pp
from pandapower.plotting import simple_plot, simple_plotly, pf_res_plotly
import pandas as pd
import matplotlib.pyplot as plt

net = pp.create_empty_network()

df= pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\FFTotal_Cluster.csv")
main_intr= pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\total_maininter.csv")
coll_intr=pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\total_collinter.csv")
intrC= pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\total_interconnection.csv")
PS=pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\total_PS.csv")

loads= pd.DataFrame()
loads= df

for i in loads.index:
  if loads.loc[i]['Population'] == 0:
        loads.drop(i,inplace=True)


df.index=df['ID']
PS.index=PS['ID']
loads.index=loads['ID']

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

#creating Primary Substations
# pp.create_bus(net, name = "start", vn_kv =110, type='b', index=0, geodata=(242930.332400000013877,8504689.038999998942018))
# pp.create_bus(net, name = "end", vn_kv =20, type='n',index=1, geodata=(214818.714399999997113,8524479.566999999806285))


##### CREATE MAIN BRANCH: BUSES & LINES ###############
# creating Secondary Substations
for i in main_idx.index:
     if(df.at[i,"Population"] == "0"):
        pp.create_bus(net, vn_kv=20, type='n', index=main_idx[i], geodata=(df.at[main_idx[i], "X"], df.at[main_idx[i], "Y"]))
     else:
        pp.create_bus(net, vn_kv=20, type='b', index=main_idx[i], geodata=(df.at[main_idx[i], "X"], df.at[main_idx[i], "Y"]))

for i in main_intr.index:
     pp.create_line(net, from_bus=main_intr.at[i, 'ID1'], to_bus=main_intr.at[i, 'ID2'], length_km=1, std_type="NAYY 4x150 SE")




##### CREATE COLLATERAL BRANCH: BUSES & LINES ###############
for i in coll_idx.index:
       if(coll_idx[i] in main_idx.index):
           coll_idx.drop(index=i, inplace=True)

for i in coll_idx.index:
         if(df.at[i,"Population"] == "0"):
            pp.create_bus(net, vn_kv=20, type='n', index=coll_idx[i], geodata=(df.at[coll_idx[i], "X"], df.at[coll_idx[i], "Y"]))
         else:
            pp.create_bus(net, vn_kv=20, type='b', index=coll_idx[i], geodata=(df.at[coll_idx[i], "X"], df.at[coll_idx[i], "Y"]))

for i in coll_intr.index:
     pp.create_line(net, from_bus=coll_intr.at[i, 'ID1'], to_bus=coll_intr.at[i, 'ID2'], length_km=1, std_type="NAYY 4x150 SE")


##### CREATE INTERCONNECTIONS LINES: BUSES & LINES ###############
for i in intrC_idx.index:
    if ((intrC_idx[i] in main_idx.index) or (intrC_idx[i] in coll_idx.index)):
        intrC_idx.drop(index=i, inplace=True)

for i in intrC_idx.index:
    if (df.at[i, "Population"] == "0"):
        pp.create_bus(net, vn_kv=20, type='n', index=coll_idx[i],
                      geodata=(df.at[intrC_idx[i], "X"], df.at[intrC_idx[i], "Y"]))
    else:
        pp.create_bus(net, vn_kv=20, type='b', index=coll_idx[i],
                      geodata=(df.at[intrC_idx[i], "X"], df.at[intrC_idx[i], "Y"]))

for i in intrC.index:
    pp.create_line(net, from_bus=intrC.at[i, 'ID1'], to_bus=intrC.at[i, 'ID2'], length_km=1,
                   std_type="NAYY 4x150 SE")

##############################################
#Creating Load
for i in loads.index:
    pp.create_load(net, loads.at[i,'ID'], p_mw=0.1)

##############################################
#creating External Grid (Slack Bus)
pp.create_bus(net, vn_kv=110, type='b', index=0, geodata=(df.at[6276, "X"], df.at[6276, "Y"]))
pp.create_ext_grid(net, 0, vm_pu = 1)
pp.create_transformer(net, hv_bus=0, lv_bus=6276,tap_pos="0.175",std_type="25 MVA 110/20 kV")


# pp.runpp(net)
# print(net.res_bus)
# pp.plotting.plot_voltage_profile(net)
# plt.show()