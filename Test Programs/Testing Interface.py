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
# output = co.COPT(SystemDef.generators)
# co.plotCOPT(output)
# print(output)

# pandapower test
# test = create_ppc()

#create_pp_from_ppc()

#print(test)


"""COPT for RTS-GMLC data"""
data = pd.read_csv(SystemDef.filepath)

# create list of individual generator outage tables
#FORs = data.loc[:, "FOR"].values
#gen = np.array([0, 1-FORs],[cap,FORs])

stuff = data.loc[:10,["PMax MW","FOR"]].values
allgens = [np.array([[0, 1-gen[1]],[gen[0], gen[1]]]) for gen in stuff]
output = co.COPT(allgens)
sumtypes = data.groupby(["Category"])["PMax MW"].sum()
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

