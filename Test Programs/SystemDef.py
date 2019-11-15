"""
Created by Jackie Baum on 11/7/19

Project Description:
System definition for Capacity Outage calculation
"""
import numpy as np

# if capacity table is read from file, do some validation on Probabilities
data = np.array([[10, 0.10, 0.90], \
                 [25, 0.02, 0.98], \
                 [40, 0.05, 0.95], \
                 [50, 0.03, 0.97]])

data2 = np.array([[25, 0.02, 0.98], \
                 [25, 0.02, 0.98], \
                 [50, 0.02, 0.98]])

gen1 = np.array([[0, 0.98],\
                 [25, 0.02]])

gen2 = np.array([[0, 0.98],\
                 [25, 0.02]])

gen3 = np.array([[0, 0.960],\
                 [20, 0.033],\
                 [50, 0.007]])

gen4 = np.array([[0, 0.98],\
                 [50, 0.02]])

gen5 = np.array([[0, 0.98],\
                 [3, 0.02]])

gen6 = np.array([[0, 0.98],\
                 [5, 0.02]])

generators = [gen1, gen2, gen3]