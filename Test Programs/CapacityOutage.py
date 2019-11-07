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
# sysRiskFig = plt.figure()
# plt.plot(SysRisk[:, 0], SysRisk[:, 2], label=unavail)
plt.xlabel('Number of Units in system')
plt.ylabel('Relative Risk (in % of 2 unit case)')
plt.legend()
plt.title("Relative Risk of using a 1 unit reserve criterion")
#plt.show() #---> UNCOMMENT TO SHOW PLOT


data = np.array([[25, 0.02, 0.98], \
                 [30, 0.02, 0.98], \
                 [50, 0.02, 0.98]])


def COPT(data):
    """
    Recursive algorithm for capacity model building (Allan and Billington, 2.2.4)
    Input: array of unit capacities and outage probabilities
    [capacity, P(unavailable), P(available)]
    Output: cumulative outage probability table
    [Capacity out, Cumulative probability]
    """
    # initalize Outage Table dataframe
    coptHeaders = ["Capacity Outage", "Cumulative Probability"]
    testdata = np.array([[0, 1.0], [25, 0.95], [50, 0.005]])
    outageTable = pd.DataFrame(data=None, columns=coptHeaders)
    outageTable = outageTable.set_index(coptHeaders[0])  # sets index to capacity outage value

    #outageTable.loc[70] = 0.0008  ## adds index 70 with given value to the data frame

    # initialize probability table --> this method seems incorrect
    outageSteps = np.linspace(0, data[:, 0].sum(), 1 + data[:, 0].sum() / data[:, 0].min())
    # outageTable = np.zeros((outageSteps.size, 2))  # update this to size based on increments of smallest unit
    # outageTable[:, 0] = outageSteps

    for unit in data:
        # make list of new outage values to calculate
            # get current index list
            # add "new unit" to each item in current index list
            # remove duplicates
        # iterate through list of new outage values and calculate new cumulative probability
            ## ?? if prev outage value exists, use it, else .... substitute?

        outageTable.loc[unit[0]] = unit[1] + 1
        print(outageTable)
        # outageTable[outageTable[:,0]==25,1] = 0.005

    return outageTable


output = COPT(data)

print("did it work?")
