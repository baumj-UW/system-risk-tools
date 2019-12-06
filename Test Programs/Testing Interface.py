"""
Created by Jackie Baum on 10/17/2019

Project Description:
This is a collection of tests and demos
"""

import scipy
import numpy as np
from pypower.api import *
import CapacityOutage as co
from RTS_Data.FormattedData.pandapower.source_data_to_pp import create_ppc, create_pp_from_ppc
import pandas as pd
import SystemDef
import time


# pypower test
#sysdata = loadcase(casefile=case9())

# """Demo Relative System risk plot"""
# outageProbs = np.linspace(0.02, 0.1, 5)
# co.relSysRisk(outageProbs)
#
# # """Demo Capacity Outage Functions"""
# start_long = time.time()
# output = co.COPT(SystemDef.generators, speed=[False, ])
# shorter = co.roundCOPT(output.copy())
# speed_long = time.time() - start_long
# print("long:",speed_long)
#
# start_short = time.time()
# short_out = co.COPT(SystemDef.generators, speed=[True, 20])
# speed_short = time.time() - start_short
# print("short:",speed_short)
#
# co.plotCOPT(output)
# co.plotCOPT(shorter)
# print(output)

# pandapower test
# test = create_ppc()

#create_pp_from_ppc()

#print(test)


"""COPT for RTS-GMLC data"""
# data = pd.read_csv(SystemDef.filepath)
#
# # create list of individual generator outage tables
# smalltable = data.loc[data.loc[:, "FOR"] > 0, ["Category","PMax MW","FOR"]] # limits data used for table
# # stuff = data.loc[:,["PMax MW","FOR"]].values
#
# fulltable = data.loc[:, ["Category","PMax MW","FOR"]] # limits data used for table
# allgens = [np.array([[0, 1-gen[2]],[gen[1], gen[2]]]) for gen in fulltable.values] #changed to test
#
#
# MAKE_COPT = False
# #for step in [10, 20, 30, 40, 50, 60, 70, 80 , 90, 100]:
# for step in [20]:
#     if MAKE_COPT:
#         start_time = time.time()
#         output = co.COPT(allgens, pmin=1e-5, speed=[True, step])
#         runtime = time.time() - start_time
#         fullpath = SystemDef.savepath +"alldata_%d_" % step + "output.csv"
#         output.to_csv(fullpath)
#         with open(fullpath, 'a') as fd:
#             fd.write("Table build-time: %f sec" % runtime)
#     else:
#         # option to read COPT from file
#         output = pd.read_csv(SystemDef.savepath + "output.csv", index_col="Capacity Outage")
#
# sumtypes = fulltable.groupby(["Category"])["PMax MW"].sum()
# co.plotCOPT(output, sumtypes)


""" Additional test functions for combining tables"""
gens = []
for path in SystemDef.datapath:
    data = pd.read_csv(path, skipfooter=1)
    gens.append(data.loc[:,["Capacity Outage", "Individual Prob"]].values)

start_time = time.time()
lrg_sys = co.COPT(gens, pmin=1e-5, speed=[True, 60])
runtime = time.time() - start_time
print(runtime)
lrg_sys.to_csv(SystemDef.savepath + "combo.csv")
with open(SystemDef.savepath + "combo.csv", 'a') as fd:
             fd.write("Table build-time: %f sec" % runtime)

co.plotCOPT(lrg_sys)
"""
random functions that might be necessary 
headers = data.columns
"""

