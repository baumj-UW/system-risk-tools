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


def COPT(data, pmin=1e-10, speed=[True, 50]):
    """
    Recursive algorithm for capacity model building (Allan and Billington, 2.2.4)
    Input: list of units in the system
            units represented by array of [Ci,Pi] for i states of outage C with probability P
            pmin - cutoff probability
            speed[T/F, int] - T/F to activate table rounding, int = table length that triggers rounding
    Output: cumulative outage probability table
    [Capacity out, Cumulative probability]
    """
    assert pmin<1, "Your cutoff pmin will return an empty table"

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

        # Round table if speed[0] is true and table is longer than speed[1]
        if speed[0] and (len(outageTable) > speed[1]):
            # calculate individual probabilities --> figure out an efficient time to do this
            outageTable = outageTable.sort_values(by='Capacity Outage')
            c_probs = outageTable.loc[:, "Cumulative Prob"].values
            i_probs = c_probs.copy()
            i_probs[0:-1] = c_probs[0:-1] - c_probs[1:]
            outageTable.loc[:, "Individual Prob"] = i_probs
            outageTable = roundCOPT(outageTable)


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
    #step_size = max(round(prev_outages[1], -1), 10) #make step size smallest gen --> could improve this
    step_size = round(prev_outages[1]+5, -1)  # make step size smallest gen --> could improve this
    new_steps = np.arange(0, prev_outages[-1]+step_size, step=step_size, dtype=int)
    init = list(set(new_steps) - set(prev_outages))
    for step in init:
        table.loc[step, "Individual Prob"] = 0 ## need to initialize for all table values

    # Proportionately split individual probabilities from old COPT to new step sizes
    # For details see Billington and Alan Ch.3
    for cap in prev_outages:
        if cap not in new_steps:
            k = bisect_left(new_steps, cap) #index of Ck, Cj = k-1
            Cj = new_steps[k-1]
            Ck = new_steps[k]
            table.loc[Cj, "Individual Prob"] += (Ck - cap)/(Ck - Cj) * table.loc[cap, "Individual Prob"]
            table.loc[Ck, "Individual Prob"] += (cap - Cj) / (Ck - Cj) * table.loc[cap, "Individual Prob"]

    # Recalculate cumulative probability based on new steps
    newtable = table.loc[new_steps].copy()
    c_probs = [newtable.loc[cap:, "Individual Prob"].values.sum() for cap in new_steps]
    newtable.loc[:, "Cumulative Prob"] = c_probs

    return newtable


def plotCOPT(table, gendata=None):
    # Plot and Print Capacity outage
    CapOutFig = plt.figure()
    plt.plot(table.loc[:,'Cumulative Prob'], label="Cumulative")
    plt.plot(table.loc[:,'Individual Prob'], label="Individual")
    plt.xlabel('Capacity Outage (MW)')
    plt.ylabel('Probability')
    plt.title("Capacity Outage Probability")
    plt.grid()
    plt.legend()

    #Plot stacked bar of generator types if given
    if gendata is not None:
        #barfig = plt.figure()
       # pivot_df = gendata.pivot(columns="Category",values="PMax MW")
        #gendata.plot.bar(stacked=True)# , figsize=(10,7))
        pd.DataFrame(gendata).T.plot.bar(stacked=True) #this is round about but works
        plt.title("Generation Mix")
        plt.ylabel("Capacity in MW")
    plt.show() #---> UNCOMMENT TO SHOW PLOT CapOutFig,barfig
    return



