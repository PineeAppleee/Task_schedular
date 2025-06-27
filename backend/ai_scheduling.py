import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import random

# --- Traditional Scheduling Algorithms ---
def fcfs(tasks):
    tasks = sorted(tasks, key=lambda x: x['arrival'])
    time = 0
    for t in tasks:
        if time < t['arrival']:
            time = t['arrival']
        t['start'] = time
        t['finish'] = time + t['burst']
        t['waiting'] = t['start'] - t['arrival']
        t['turnaround'] = t['finish'] - t['arrival']
        time += t['burst']
    return tasks

def sjf(tasks):
    tasks = sorted(tasks, key=lambda x: (x['arrival'], x['burst']))
    time = 0
    completed = []
    ready = []
    idx = 0
    n = len(tasks)
    while len(completed) < n:
        while idx < n and tasks[idx]['arrival'] <= time:
            ready.append(tasks[idx])
            idx += 1
        if ready:
            ready.sort(key=lambda x: x['burst'])
            t = ready.pop(0)
            t['start'] = time
            t['finish'] = time + t['burst']
            t['waiting'] = t['start'] - t['arrival']
            t['turnaround'] = t['finish'] - t['arrival']
            time += t['burst']
            completed.append(t)
        else:
            time = tasks[idx]['arrival']
    return completed

def round_robin(tasks, quantum=2):
    queue = []
    time = 0
    idx = 0
    n = len(tasks)
    tasks = sorted(tasks, key=lambda x: x['arrival'])
    for t in tasks:
        t['remaining'] = t['burst']
        t['finish'] = 0
        t['waiting'] = 0
        t['turnaround'] = 0
        t['start'] = -1
    completed = 0
    last_finish = [0]*n
    while completed < n:
        while idx < n and tasks[idx]['arrival'] <= time:
            queue.append(tasks[idx])
            idx += 1
        if not queue:
            time = tasks[idx]['arrival']
            continue
        t = queue.pop(0)
        if t['start'] == -1:
            t['start'] = time
        exec_time = min(quantum, t['remaining'])
        t['remaining'] -= exec_time
        time += exec_time
        while idx < n and tasks[idx]['arrival'] <= time:
            queue.append(tasks[idx])
            idx += 1
        if t['remaining'] == 0:
            t['finish'] = time
            t['waiting'] = t['finish'] - t['arrival'] - t['burst']
            t['turnaround'] = t['finish'] - t['arrival']
            completed += 1
        else:
            queue.append(t)
    return tasks

# --- Feature Extraction for AI ---
def extract_features(tasks):
    burst_times = [t['burst'] for t in tasks]
    arrival_times = [t['arrival'] for t in tasks]
    priority_values = [t.get('priority', 3) for t in tasks]  # Default priority=3 if not present
    features = [
        len(tasks),
        np.mean(burst_times),
        np.std(burst_times),
        np.mean(arrival_times),
        np.std(arrival_times),
        np.min(burst_times),
        np.max(burst_times),
        np.min(arrival_times),
        np.max(arrival_times),
        np.mean(priority_values),
        np.std(priority_values)
    ]
    return np.array(features).reshape(1, -1)

# --- AI Model Training (Synthetic Data) ---
def generate_synthetic_data(samples=500):
    X = []
    y = []
    for _ in range(samples):
        n = random.randint(3, 15)
        bursts = np.random.randint(1, 20, n)
        arrivals = np.sort(np.random.randint(0, 10, n))
        features = [n, np.mean(bursts), np.std(bursts), np.mean(arrivals), np.std(arrivals), np.min(bursts), np.max(bursts), np.min(arrivals), np.max(arrivals)]
        # Simulate which algo is best: SJF for high burst std, RR for high arrival std, FCFS otherwise
        if np.std(bursts) > 5:
            label = 1  # SJF
        elif np.std(arrivals) > 3:
            label = 2  # RR
        else:
            label = 0  # FCFS
        X.append(features)
        y.append(label)
    return np.array(X), np.array(y)

algo_names = ['FCFS', 'SJF', 'RR']

# --- Main Script ---
def main():
    print("\n--- AI-Enhanced Task Scheduling ---\n")
    num_tasks = input("Enter number of tasks (default 5): ")
    try:
        num_tasks = int(num_tasks)
    except:
        num_tasks = 5
    bursts = np.random.randint(1, 20, num_tasks)
    arrivals = np.sort(np.random.randint(0, 10, num_tasks))
    print("Generated burst times:", bursts)
    print("Generated arrival times:", arrivals)
    tasks = [{'tid': i+1, 'burst': int(bursts[i]), 'arrival': int(arrivals[i]), 'priority': random.randint(1, 5)} for i in range(num_tasks)]

    # Run all algorithms
    fcfs_result = fcfs([t.copy() for t in tasks])
    sjf_result = sjf([t.copy() for t in tasks])
    rr_result = round_robin([t.copy() for t in tasks], quantum=2)

    # Collect metrics
    def get_metrics(result):
        avg_wait = np.mean([t['waiting'] for t in result])
        avg_turn = np.mean([t['turnaround'] for t in result])
        return avg_wait, avg_turn
    metrics = [get_metrics(fcfs_result), get_metrics(sjf_result), get_metrics(rr_result)]

    print("\n--- Results ---")
    for i, name in enumerate(algo_names):
        print(f"{name}: Avg Waiting = {metrics[i][0]:.2f}, Avg Turnaround = {metrics[i][1]:.2f}")

    # --- AI Model: Load real dataset ---
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier

    df = pd.read_csv('scheduling_dataset.csv')
    features = [
        'num_tasks','burst_mean','burst_std','arrival_mean','arrival_std',
        'burst_min','burst_max','arrival_min','arrival_max','priority_mean','priority_std'
    ]
    X = df[features]
    y = df['best_algo']

    model = RandomForestClassifier()
    model.fit(X, y)
    # Save model if needed
    import joblib
    joblib.dump(model, 'scheduling_model.pkl')
    # Extract features from current task set
    def extract_features(tasks):
        burst_times = [t['burst'] for t in tasks]
        arrival_times = [t['arrival'] for t in tasks]
        priority_values = [t.get('priority', 3) for t in tasks]  # Default priority=3 if not present
        features = [
            len(tasks),
            np.mean(burst_times),
            np.std(burst_times),
            np.mean(arrival_times),
            np.std(arrival_times),
            np.min(burst_times),
            np.max(burst_times),
            np.min(arrival_times),
            np.max(arrival_times),
            np.mean(priority_values),
            np.std(priority_values)
        ]
        return np.array(features).reshape(1, -1)
    features = extract_features(tasks)
    pred = model.predict(features)[0]
    print(f"\nAI Recommendation: Use {algo_names[pred]} for this task set!\n")

    # Optional: Show detailed table
    df_tasks = pd.DataFrame(tasks)
    df_tasks['FCFS_Wait'] = [t['waiting'] for t in fcfs_result]
    df_tasks['SJF_Wait'] = [t['waiting'] for t in sjf_result]
    df_tasks['RR_Wait'] = [t['waiting'] for t in rr_result]
    print(df_tasks)

if __name__ == "__main__":
    main()