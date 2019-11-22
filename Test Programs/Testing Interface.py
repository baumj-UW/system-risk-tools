"""
Created by Jackie Baum on 10/17/2019

Project Description:
This is a collection of tests and demos
"""

import scipy
from pypower.api import *
#import CapacityOutage
from RTS_Data.FormattedData.pandapower.source_data_to_pp import create_ppc, create_pp_from_ppc


sysdata = loadcase(casefile=case9())

test = create_ppc()

create_pp_from_ppc()

print(test)

#pd.read_csv(start_path + table + ".csv")