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



sysdata = loadcase(casefile=case9())

"""Demo Relative System risk plot"""
outageProbs = np.linspace(0.02, 0.1, 5)
co.relSysRisk(outageProbs)

"""Demo Capacity Outage Functions"""
output = co.COPT(SystemDef.generators)
co.plotCOPT(output)
print(output)



test = create_ppc()

#create_pp_from_ppc()

#print(test)

data = pd.read_csv(SystemDef.filepath)

"""
random functions that might be necessary 
headers = data.columns
"""

