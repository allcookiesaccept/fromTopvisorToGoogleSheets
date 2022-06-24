import pandas as pd
import numpy as np

olap = pd.read_excel('olap_channels.xlsx')

print(olap)
period = ['year', 'month']
channels = ['(none)', '(not set)', 'cpc', 'email', 'NA', 'organic', 'referral', 'trigger']
metrics = ['orders', 'revenue', 'aov', 'profit']

direct_orders_sum = olap['(none)-orders'] + olap['(not set)-orders']

# df = pd.read_csv('ex.txt', delimiter='\t')

print(olap.columns)

channels_metrics = []
for channel in channels:
    for metric in metrics:
        channels_metrics.append(f'{channel}-{metric}')

headers = [*period, *channels_metrics]

for index, row in olap.iterrows():
    print(index, row['year'])

