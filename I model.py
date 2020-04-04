# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 16:12:21 2019

@author: Silvia
"""

from __future__ import division

from pyomo.opt import SolverFactory
from pyomo.core import AbstractModel
from pyomo.dataportal.DataPortal import DataPortal
from pyomo.environ import *
import pandas as pd
from datetime import datetime
############ Create abstract model ###########
model = AbstractModel()
data = DataPortal()

# ####################Define sets#####################

#Name of all the nodes (primary and secondary substations)
model.N=Set()
data.load(filename='nodes.csv', set=model.N) #first row is not read

#Node corresponding to primary substation
model.PS=Set(within=model.N)
data.load(filename='PS.csv',set=model.PS)
#Allowed connections
model.links=Set(dimen=2) #in the csv the values must be delimited by commas
data.load(filename='links.csv', set=model.links)

#Nodes are divided into two sets, as suggested in https://pyomo.readthedocs.io/en/stable/pyomo_modeling_components/Sets.html:
# NodesOut[nodes] gives for each node all nodes that are connected to it via outgoing links
# NodesIn[nodes] gives for each node all nodes that are connected to it via ingoing links

def NodesOut_init(model, node):
    retval = []
    for (i,j) in model.links:
        if i == node:
            retval.append(j)
    return retval
model.NodesOut = Set(model.N, initialize=NodesOut_init)

def NodesIn_init(model, node):
    retval = []
    for (i,j) in model.links:
        if j == node:
            retval.append(i)
    return retval
model.NodesIn = Set(model.N, initialize=NodesIn_init)


#####################Define parameters#####################

#Electric power in the nodes (injected (-) or absorbed (+))
model.Psub=Param(model.N)
data.load(filename='power.csv', param=model.Psub)

#Power of the primary substation as sum of all the other powers
def PPS_init(model):
    return sum(model.Psub[i] for i in model.N)
model.PPS=Param(model.PS,initialize=PPS_init)

#Connection distance of all the edges
model.dist=Param(model.links)
data.load(filename='distances.csv', param=model.dist)

#Electrical parameters of all the cables
model.V_ref=Param()
model.A_ref=Param()
model.R_ref=Param()
model.X_ref=Param()
model.P_max=Param()
model.cf=Param()
model.E_min=Param()
model.E_max=Param()

data.load(filename='data.dat')

#Resistance and reactance of each edge
def R_l_creation(model,i,j):
    return model.dist[i,j]*model.R_ref*model.A_ref/model.V_ref**2/1000

def X_l_creation(model,i,j):
    return model.dist[i,j]*model.X_ref*model.A_ref/model.V_ref**2/1000

model.R_l=Param(model.links,initialize=R_l_creation)
model.X_l=Param(model.links,initialize=X_l_creation)
#M_max and M_min, values required to linearize the problem
model.M_max=Param(initialize=10)
model.M_min=Param(initialize=-10)


#####################Define variables#####################

#binary variable x[i,j]: 1 if the connection i,j is present, 0 otherwise
model.x = Var(model.links, within=Binary)
#power[i,j] is the power flow of connection i-j
model.P = Var(model.links)
#positive variables E(i) is p.u. voltage at each node
model.E = Var(model.N,within=NonNegativeReals)
#variables z(i,j) is the variable necessary to linearize
model.z = Var(model.links)

#####################Define constraints###############################

#def Radiality_rule(model):
#    return summation(model.x)==len(model.N)-1
#model.Radiality = Constraint(rule=Radiality_rule)

def Power_flow_conservation_rule(model,node):
    return (sum(model.P[j,node]for j in model.NodesIn[node])-sum(model.P[node,j] for j in model.NodesOut[node]))==model.Psub[node]
model.Power_flow_conservation = Constraint(model.N, rule=Power_flow_conservation_rule)

def Power_upper_bounds_rule(model,i,j):
    return model.P[i,j] <= model.P_max*model.x[i,j]
model.upper_Power_limits = Constraint(model.links, rule=Power_upper_bounds_rule)

def Power_lower_bounds_rule(model,i,j):
    return model.P[i,j] >= -model.P_max*model.x[i,j]
model.lower_Power_limits = Constraint(model.links, rule=Power_upper_bounds_rule)

#Voltage constraints
def Voltage_balance_rule(model,i,j):
    return model.z[i,j]==(model.R_l[i,j]*model.P[i,j]+model.X_l[i,j]*0.5*model.P[i,j])/model.A_ref
model.Voltage_balance_rule=Constraint(model.links,rule=Voltage_balance_rule)

def Voltage_linearization_rule_1(model,i,j):
    return model.z[i,j]<=model.M_max*model.x[i,j]
model.Voltage_linearization_rule_1=Constraint(model.links, rule=Voltage_linearization_rule_1)

def Voltage_linearization_rule_2(model,i,j):
    return model.z[i,j]>=model.M_min*model.x[i,j]
model.Voltage_linearization_rule_2=Constraint(model.links, rule=Voltage_linearization_rule_2)

def Voltage_linearization_rule_3(model,i,j):

    return model.E[i]-model.E[j]-(1-model.x[i,j])*model.M_max <= model.z[i,j]
model.Voltage_linearization_rule_3=Constraint(model.links, rule=Voltage_linearization_rule_3)

def Voltage_linearization_rule_4(model,i,j):
    return model.E[i]-model.E[j]-(1-model.x[i,j])*model.M_min >= model.z[i,j]
model.Voltage_linearization_rule_4=Constraint(model.links, rule=Voltage_linearization_rule_4)

def Voltage_linearization_rule_5(model,i,j):
    return model.E[i]-model.E[j]+(1-model.x[i,j])*model.M_max >= model.z[i,j]
model.Voltage_linearization_rule_5=Constraint(model.links, rule=Voltage_linearization_rule_5)

def Voltage_lower_bound_rule(model,i):
    return model.E_min<=model.E[i]
model.Voltage_lower_bound=Constraint(model.N,rule=Voltage_lower_bound_rule)

def Voltage_upper_bound_rule(model,i):
    return model.E_max>=model.E[i]
model.Voltage_upper_bound=Constraint(model.N,rule=Voltage_upper_bound_rule)

def Voltage_primary_substation_rule(model,i):
    return model.E[i]==1
model.Voltage_primary_substation=Constraint(model.PS,rule=Voltage_primary_substation_rule)

####################Define objective function##########################

def ObjectiveFunction(model):
    return summation(model.dist,model.x)*model.cf/1000
model.Obj = Objective(rule=ObjectiveFunction, sense=minimize)

#############Solve model##################

instance = model.create_instance(data)
print('Instance is constructed:', instance.is_constructed())
#opt = SolverFactory('cbc',executable=r'C:\Users\Asus\Desktop\POLIMI\Thesis\GISELE\Gisele_MILP\cbc')
opt = SolverFactory('gurobi')
opt.options['mipgap'] = 0.4

#opt = SolverFactory('cbc',executable=r'C:\Users\Asus\Desktop\POLIMI\Thesis\GISELE\New folder\cbc')
print('Starting optimization process')
time_i=datetime.now()
opt.solve(instance,tee=True)
time_f=datetime.now()
print('Time required for optimization is', time_f-time_i)
links=instance.x
power=instance.P
connections_output=pd.DataFrame(columns=[['id1','id2']])
k=0
for index in links:
    if int(round(value(links[index])))==1:
        connections_output.loc[k,'id1']=index[0]
        connections_output.loc[k,'id2']=index[1]
        k=k+1

connections_output.to_csv('connections_output.csv')
