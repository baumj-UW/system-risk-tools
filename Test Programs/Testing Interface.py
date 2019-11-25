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


# pypower test
#sysdata = loadcase(casefile=case9())

# """Demo Relative System risk plot"""
# outageProbs = np.linspace(0.02, 0.1, 5)
# co.relSysRisk(outageProbs)
#
# """Demo Capacity Outage Functions"""
output = co.COPT(SystemDef.generators, speed=[False, ])
short_out = co.COPT(SystemDef.generators, speed=[True, 20])
shorter = co.roundCOPT(output.copy())
co.plotCOPT(output)
co.plotCOPT(shorter)
# print(output)

# pandapower test
# test = create_ppc()

#create_pp_from_ppc()

#print(test)


"""COPT for RTS-GMLC data"""
data = pd.read_csv(SystemDef.filepath)

# create list of individual generator outage tables
smalltable = data.loc[data.loc[:, "FOR"] > 0, ["Category","PMax MW","FOR"]] # limits data used for table
# stuff = data.loc[:,["PMax MW","FOR"]].values
allgens = [np.array([[0, 1-gen[2]],[gen[1], gen[2]]]) for gen in smalltable.values]


MAKE_COPT = False
if MAKE_COPT:
    output = co.COPT(allgens, pmin=1e-7) #save this to a file for using later
    output.to_csv(SystemDef.savepath + "output.csv")
else:
    # option to read COPT from file
    output = pd.read_csv(SystemDef.savepath + "output.csv", index_col="Capacity Outage")

sumtypes = smalltable.groupby(["Category"])["PMax MW"].sum()
co.plotCOPT(output, sumtypes)

# for gen in stuff:
#     table = [np.array([[0, 1-gen[1]],[gen[0], gen[1]]])]
# for i in data:
#     gen = np.array([[0, 1-FOR],\
#                     [P MaxMW, FOR]])
"""
random functions that might be necessary 
headers = data.columns
"""

