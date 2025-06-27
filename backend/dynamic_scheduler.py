import time
import threading
import random
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# --- Scheduling Algorithms ---
def fcfs(tasks):
    tasks = sorted(tasks, key=lambda x: x['arrival'])
    time_marker = 0
    for t in tasks:
        if time_marker < t['arrival']:
            time_marker = t['arrival']
        t['start'] = time_marker
        t['finish'] = time_marker + t['burst']
        t['waiting'] = t['start'] - t['arrival']
        t['turnaround'] = t['finish'] - t['arrival']
        time_marker += t['burst']
    return tasks

def sjf(tasks):
    tasks = sorted(tasks, key=lambda x: (x['arrival'], x['burst']))
    time_marker = 0
    completed = []
    ready = []
    idx = 0
    n = len(tasks)
    while len(completed) < n:
        while idx < n and tasks[idx]['arrival'] <= time_marker:
            ready.append(tasks[idx])
            idx += 1
        if ready:
            ready.sort(key=lambda x: x['burst'])
            t = ready.pop(0)
            t['start'] = time_marker
            t['finish'] = time_marker + t['burst']
            t['waiting'] = t['start'] - t['arrival']
            t['turnaround'] = t['finish'] - t['arrival']
            time_marker += t['burst']
            completed.append(t)
        else:
            time_marker = tasks[idx]['arrival']
    return completed

def round_robin(tasks, quantum=2):
    queue = []
    time_marker = 0
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
    while completed < n:
        while idx < n and tasks[idx]['arrival'] <= time_marker:
            queue.append(tasks[idx])
            idx += 1
        if not queue:
            time_marker = tasks[idx]['arrival']
            continue
        t = queue.pop(0)
        if t['start'] == -1:
            t['start'] = time_marker
        exec_time = min(quantum, t['remaining'])
        t['remaining'] -= exec_time
        time_marker += exec_time
        while idx < n and tasks[idx]['arrival'] <= time_marker:
            queue.append(tasks[idx])
            idx += 1
        if t['remaining'] == 0:
            t['finish'] = time_marker
            t['waiting'] = t['finish'] - t['arrival'] - t['burst']
            t['turnaround'] = t['finish'] - t['arrival']
            completed += 1
        else:
            queue.append(t)
    return tasks

# --- AI Model Setup ---
def extract_features(tasks):
    burst_times = [t['burst'] for t in tasks]
    arrival_times = [t['arrival'] for t in tasks]
    features = [
        len(tasks),
        np.mean(burst_times),
        np.std(burst_times),
        np.mean(arrival_times),
        np.std(arrival_times),
        np.min(burst_times),
        np.max(burst_times),
        np.min(arrival_times),
        np.max(arrival_times)
    ]
    return np.array(features).reshape(1, -1)

df = pd.read_csv('scheduling_dataset.csv')
X = df.drop('best_algo', axis=1).values
y = df['best_algo'].values
clf = RandomForestClassifier(n_estimators=50, random_state=42)
clf.fit(X, y)
algo_names = ['FCFS', 'SJF', 'RR']


task_queue = []
lock = threading.Lock()

def scheduler_loop():
    while True:
        with lock:
            if task_queue:
                print("\nRescheduling with current tasks:")
                for t in task_queue:
                    print(t)
                features = extract_features(task_queue)
                pred = clf.predict(features)[0]
                print(f"\nAI Recommendation: {algo_names[pred]}")
                if pred == 0:
                    result = fcfs([t.copy() for t in task_queue])
                elif pred == 1:
                    result = sjf([t.copy() for t in task_queue])
                else:
                    result = round_robin([t.copy() for t in task_queue], quantum=2)
                print("\nSchedule:")
                for t in result:
                    print(f"Task {t['tid']}: Start={t['start']} Finish={t['finish']} Waiting={t['waiting']}")
                task_queue.clear()
        time.sleep(5) 

def add_task():
    tid = 1
    while True:
        user = input("Add new task? (y/n or 'stop' to exit): ")
        if user.lower() == 'stop':
            print("Stopping scheduler as requested.")
            exit(0)
        if user.lower() == 'y':
            burst = random.randint(1, 20)
            arrival = int(time.time()) % 100  
            with lock:
                task_queue.append({'tid': tid, 'burst': burst, 'arrival': arrival})
            print(f"Added Task {tid} (burst={burst}, arrival={arrival})")
            tid += 1

if __name__ == "__main__":
    threading.Thread(target=scheduler_loop, daemon=True).start()
    add_task()