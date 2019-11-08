"""
Created by Jackie Baum on 10/25/2019

Project Description:
Calculate the capacity outage probability table
Display relative risk calculations
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.misc
import pandas as pd

# define probabilities


unavail = 0.02


def calcSysRisk(unavail):
    """
    Calculates the relative system risk at given unavailability
    Returns table of system risk (like Table 3.13 in Billington text)
    """
    P = np.array([[unavail, (1 - unavail)]])
    # calculate system relative risk table (3.13 from Reliability Engineering)
    NUM_UNITS = 10  # number of units in the system
    REF_UNITS = 2  # number of units used as baseline for relative risk
    SysRisk = np.zeros((NUM_UNITS + 1, 3))  # Table columns [# units, P(2+ unit outage), Relative risk]
    for units in range(2, NUM_UNITS + 1, 1):
        SysRisk[units, 0] = units
        SysRisk[units, 1] = 1 - (P[0, 1] ** (units - 1) * (P[0, 1] + units * P[0, 0]))
        SysRisk[units, 2] = SysRisk[units, 1] / SysRisk[REF_UNITS, 1]
        # scipy.misc.comb(5,2)

    return SysRisk


# Plot relative risk
sysRiskFig = plt.figure()
# Calculate relative system risk for range of outage probabilities
outageProbs = np.linspace(0.02, 0.1, 5)
SysRiskList = []
for val in outageProbs:
    SysRisk = calcSysRisk(val)
    plt.plot(SysRisk[:, 0], SysRisk[:, 2], label=val)
    # SysRiskList.append(calcSysRisk(val)) #creates a list of each risk table

# Plot relative risk
plt.xlabel('Number of Units in system')
plt.ylabel('Relative Risk (in % of 2 unit case)')
plt.legend()
plt.title("Relative Risk of using a 1 unit reserve criterion")
# plt.show() #---> UNCOMMENT TO SHOW PLOT


# if capacity table is read from file, do some validation on Probabilities
data = np.array([[10, 0.10, 0.90], \
                 [25, 0.02, 0.98], \
                 [40, 0.05, 0.95], \
                 [50, 0.03, 0.97]])


def COPT(data):
    """
    Recursive algorithm for capacity model building (Allan and Billington, 2.2.4)
    Input: array of unit capacities and outage probabilities
    [capacity, P(unavailable), P(available)]
    Output: cumulative outage probability table
    [Capacity out, Cumulative probability]
    """
    # initalize Outage Table dataframe with P(0) = 1.0
    coptHeaders = ["Capacity Outage", "Cumulative Prob"]
    outageTable = pd.DataFrame(data=np.array([[0, 1.0]]), columns=coptHeaders)
    outageTable = outageTable.set_index(coptHeaders[0])  # sets index to capacity outage value

    for unit in data:
        # make list of new outage values to calculate
        prev_out = list(outageTable.index.values)
        new_out = [unit[0] + x for x in prev_out]  # add "new unit" to each item in current index list
        new_out.extend(x for x in prev_out if x not in new_out)  # maybe keep separate lists?
        new_out.sort()  # sorts this list (not needed) --> better to wait until final table is complete
        new_probs = []
        for outage in new_out:  # recursive capacity add per Billington
            x_c = ({True: (outage - unit[0]), False: 0}[(outage - unit[0]) > 0])  # Case for negative X-C
            # P(x) = (1-U)P'(X) + (U)P'(X-C)
            prob = unit[2] * getP(outage, outageTable, prev_out) + unit[1] * getP(x_c, outageTable, prev_out)
            new_probs.append(prob)
            # could handle this addition with a for loop?# current P calc is inefficient but cleaner
        # update outage table with new probabilities
        for (x, p) in zip(new_out, new_probs):
            outageTable.loc[x, "Cumulative Prob"] = p

        print(outageTable)

    return outageTable


def getP(x, table, prev_out):
    """
    Return P'(X) if previously calculated; else P'(X) = 0
    """
    if x in prev_out:
        p = table.loc[x, "Cumulative Prob"]
    else:
        p = 0
    return p


output = COPT(data)

# Plot Capacity outage
CapOutFig = plt.figure()
plt.plot(output.sort_values(by='Capacity Outage'))
plt.xlabel('Capacity Outage')
plt.ylabel('Cumulative Probability')
plt.title("Capacity Outage Probability")
plt.grid()
#plt.show() #---> UNCOMMENT TO SHOW PLOT



