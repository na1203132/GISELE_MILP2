

import pandapower as pp
from pandapower.plotting import simple_plot, simple_plotly, pf_res_plotly
import pandas as pd
import matplotlib.pyplot as plt

net = pp.create_empty_network()

df= pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\cluster3_PS.csv")
grid= pd.read_csv(r"C:\Users\Asus\Documents\GitHub\Gisele_MILP\connections_output.csv")

SS=pd.DataFrame(df)

for i in SS.index:
  if (df.loc[i]['Population'] == 0) | (df.loc[i]['PS'] == 1):
        SS.drop(i,inplace=True)





##############################################
#creating Primary Substations
pp.create_bus(net, name = "110 kV bar", vn_kv =110, type='b', index=0, geodata=(840689.518725477973931,8509568.724492659792304))
pp.create_bus(net, name = "20 kV bar", vn_kv =20, type='b',index=grid.at[0,"id1"], geodata=(840689.518725477973931,8509568.724492659792304))


##############################################
#creating Secondary Substations
for i in SS.index:
    pp.create_bus(net, vn_kv=20, type='b',index= SS.at[i,"id"], geodata=(SS.at[i,"X"], SS.at[i,"Y"]))


##############################################
#creating External Grid (Slack Bus)
pp.create_ext_grid(net, 0, vm_pu = 1)


##############################################
#Creating Grid connections
for i in grid.index:
   pp.create_line(net, from_bus=grid.at[i,"id1"], to_bus=grid.at[i,"id2"], length_km=1, std_type="NAYY 4x50 SE")

##############################################
#Creating Transformer
#pp.create_transformer_from_parameters(net, hv_bus=0, lv_bus=grid.at[0, "id1"], i0_percent=0.038, pfe_kw=11.6, vkr_percent=0.322, sn_mva=40, vn_lv_kv=20.0, vn_hv_kv=110.0, vk_percent=17.8)
pp.create_transformer(net, hv_bus=0, lv_bus=grid.at[0, "id1"], std_type="25 MVA 110/20 kV")


##############################################
#Creating Load
for i in SS.index:
    pp.create_load(net, SS.at[i,'id'], p_mw=0.1)


pp.runpp(net)
print(net.res_bus)
#pp.plotting.plotly.geo_data_to_latlong(net, projection='epsg:5858')
pp.plotting.plotly.mapbox_plot.set_mapbox_token('pk.eyJ1IjoibmExMjAzMTMyIiwiYSI6ImNrYW9qYThxMzFvb3cyc3A2cWJyaHdhdTMifQ.bfRDDy-DV4-VuVWjDNzodg')

simple_plotly(net)
pp.plotting.plot_voltage_profile(net)
plt.show()
pp.to_excel(net, "example2.xlsx")