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
# import SystemDef as system
from bisect import bisect_left



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


def relSysRisk(outageProbs):
    # Plot relative risk
    sysRiskFig = plt.figure()
    # Calculate relative system risk for range of outage probabilities
    #outageProbs = np.linspace(0.02, 0.1, 5)
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
    plt.show(sysRiskFig) #---> UNCOMMENT TO SHOW PLOT
    return


def COPT(data, pmin=1e-10):
    """
    Recursive algorithm for capacity model building (Allan and Billington, 2.2.4)
    Input: list of units in the system
            units represented by array of [Ci,Pi] for i states of outage C with probability P
    Output: cumulative outage probability table
    [Capacity out, Cumulative probability]
    """
    # initalize Outage Table dataframe with P(0) = 1.0
    coptHeaders = ["Capacity Outage", "Cumulative Prob", "Individual Prob"]
    outageTable = pd.DataFrame(data=np.array([[0, 1.0, 1.0]]), columns=coptHeaders)
    outageTable = outageTable.set_index(coptHeaders[0])  # sets index to capacity outage value

    for unit in data:
        # make list of new outage values to calculate
        prev_out = list(outageTable.index.values)
        prev_out.sort() # sort this for processing later steps
        # new list by adding outage state Ci to each index item in existing table
        new_out = [(c + x) for c in list(unit[1:, 0]) for x in prev_out]
        new_out.extend(x for x in prev_out if x not in new_out)  # maybe keep separate lists?
        # new_out.sort()  # sorts this list (not needed) --> better to wait until final table is complete
        new_probs = []
        for outage in new_out:  # recursive capacity add per Billington
            # P(x) = sum(p_i*P'(X-C_i)) for all capacity states i
            prob = 0  # initialize new probability calc
            for (c, p) in unit:
                x = ({True: (outage - c), False: 0}[(outage - c) > 0])  # Case for negative X-C
                prob += p * getP(x, outageTable, prev_out)
                # prob += p * ({True: outageTable.loc[x, "Cumulative Prob"], False: 0}[(x in prev_out)]) # this fails

            new_probs.append(prob)
        # update outage table with new probabilities
        for (x, p) in zip(new_out, new_probs):
            outageTable.loc[x, "Cumulative Prob"] = p

        # Truncate table to save computation time
        outageTable = outageTable.loc[outageTable.loc[:, "Cumulative Prob"] > pmin]

        # print(outageTable) # Uncomment to show recursive COPT table updates

    # calculate individual probabilities
    outageTable = outageTable.sort_values(by='Capacity Outage')
    c_probs = outageTable.loc[:, "Cumulative Prob"].values
    i_probs = c_probs.copy()
    i_probs[0:-1] = c_probs[0:-1] - c_probs[1:]
    outageTable.loc[:, "Individual Prob"] = i_probs

    #print(outageTable)

    return outageTable


def getP(x, table, prev_out):
    """
    prev_out: sorted list of previous outages
    Return P'(X) if (X <= existing table values); else P'(X) = 0
    """
    if x <= prev_out[-1]:
        min_val = prev_out[bisect_left(prev_out, x)]
        p = table.loc[min_val, "Cumulative Prob"]
    else:
        p = 0

    return p


def roundCOPT(table):
    """
    General function to round the COPT
    Based on expression from Billington and Allan
    returns rounded COPT
    """
    prev_outages = table.index.values.copy()
   # np.linspace(0, prev_outages[-1], num=round(maxval/prev_outages[1])+1)
    #steps, size = np.linspace(0, table.index.values[-1], dtype=int, retstep=True)
    step_size = prev_outages[1]
    new_steps = np.arange(0, prev_outages[-1]+step_size, step=step_size, dtype=int)
    newtable = table.copy()
    table.loc[new_steps[-1], "Individual Prob"] = 0
    # c_probs = outageTable.loc[:, "Cumulative Prob"].values
    # i_probs = c_probs.copy()
    # i_probs[0:-1] = c_probs[0:-1] - c_probs[1:]
    # outageTable.loc[:, "Individual Prob"] = i_probs


    #get Ck and Cj from new_steps
    for cap in prev_outages:
        if cap not in new_steps:
            k = bisect_left(new_steps, cap) #index of Ck, Cj = k-1
            if k>0:
                Cj = new_steps[k-1]
                Ck = new_steps[k]
                table.loc[Cj, "Individual Prob"] += (Ck - cap)/(Ck - Cj) * table.loc[cap, "Individual Prob"]
                table.loc[Ck, "Individual Prob"] += (cap - Cj) / (Ck - Cj) * table.loc[cap, "Individual Prob"]
            else:
                print("it happened")
    # minval = prev_out[bisect_left(prev_out, x)]
    # P[j] = (C[k] - C[i])/(C[k] - C[j]) * P[i]
    # newtable = range(0, table.loc[-1, "Capacity Outage"].value, step=round(table.loc[1,"Capacity Outage"]))
    c_probs = [table.loc[cap:, "Individual Prob"].values.sum() for cap in new_steps]
    table.loc[new_steps, "Cumulative Prob"] = c_probs
    return table.loc[new_steps]


def plotCOPT(table, gendata):
    # Plot and Print Capacity outage
    CapOutFig = plt.figure()
    plt.plot(table, label=["Cumulative", "Individual"])
    plt.xlabel('Capacity Outage')
    plt.ylabel('Cumulative Probability')
    plt.title("Capacity Outage Probability")
    plt.grid()
    plt.legend()

    #barfig = plt.figure()
   # pivot_df = gendata.pivot(columns="Category",values="PMax MW")
    #gendata.plot.bar(stacked=True)# , figsize=(10,7))
    pd.DataFrame(gendata).T.plot.bar(stacked=True) #this is round about but works
    plt.title("Generation Mix")
    plt.ylabel("Capacity in MW")
    plt.show() #---> UNCOMMENT TO SHOW PLOT CapOutFig,barfig
    return



