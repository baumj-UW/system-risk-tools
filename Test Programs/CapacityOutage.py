"""
Created by Jackie Baum on 10/25/2019

Project Description:
Calculate the capacity outage probability table
Display relative risk calculations
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.misc

# define probabilities


unavail = 0.02
P = np.array([[unavail, (1-unavail)]])

#calculate system relative risk table (3.13 from Reliability Engineering)
NUM_UNITS = 10 #number of units in the system
REF_UNITS = 2  #number of units used as baseline for relative risk
SysRisk = np.zeros((NUM_UNITS + 1, 3)) # Table columns [# units, P(2+ unit outage), Relative risk]
for units in range(2, NUM_UNITS+1, 1):
    SysRisk[units, 0] = units
    SysRisk[units, 1] = 1 - (P[0, 1] ** (units - 1) * (P[0, 1] + units * P[0, 0]))
    SysRisk[units, 2] = SysRisk[units, 1]/SysRisk[REF_UNITS, 1]
    # scipy.misc.comb(5,2)

#Plot relative risk
sysRiskFig = plt.figure()
plt.plot(SysRisk[:, 0], SysRisk[:, 2], label=unavail)
plt.xlabel('Number of Units')
plt.ylabel('Relative Risk')
plt.legend()
plt.show()
# for (i,s) in enumerate(STATES):
#     plt.plot(results.t/365,results.y[i],label=s)
# plt.grid(True)
# plt.xlabel('Time (years)')
# plt.ylabel('Prob of being in state')
# plt.legend()
# plt.title(comp_name + " State probabilities over time")

print("did it work?")