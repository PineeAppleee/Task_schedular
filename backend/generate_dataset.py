import numpy as np
import pandas as pd
import random

rows = []
samples_per_algo = 666  # For ~2000 total rows, adjust as needed
algos = [0, 1, 2]  # 0: FCFS, 1: SJF, 2: RR

for algo in algos:
    for _ in range(samples_per_algo):
        n = random.randint(3, 15)
        bursts = np.random.randint(1, 20, n)
        arrivals = np.sort(np.random.randint(0, 10, n))
        priorities = np.random.randint(1, 6, n)  # Priority from 1 (highest) to 5 (lowest)
        features = [
            n,
            np.mean(bursts),
            np.std(bursts),
            np.mean(arrivals),
            np.std(arrivals),
            np.min(bursts),
            np.max(bursts),
            np.min(arrivals),
            np.max(arrivals),
            np.mean(priorities),
            np.std(priorities)
        ]
        row = features + [algo]
        rows.append(row)

columns = [
    'num_tasks','burst_mean','burst_std','arrival_mean','arrival_std',
    'burst_min','burst_max','arrival_min','arrival_max','priority_mean','priority_std','best_algo'
]
df = pd.DataFrame(rows, columns=columns)
df.to_csv('scheduling_dataset.csv', index=False)
print('Dataset saved as scheduling_dataset.csv with priority feature and balanced classes')