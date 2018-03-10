import csv
import numpy as np
import pandas as pd

battalionCount = [0,0,0,0,0,0,0,0,0]
df = pd.read_csv('./sfpd-dispatch/sfpd_dispatch_data_subset.csv')

for index, row in df.iterrows():
     battalion = row['battalion']
     battalion = battalion[2:]
     battalionCount[int(battalion) - 1] = battalionCount[int(battalion) - 1] + 1

print(battalionCount)




