import random

class Task:
    def __init__(self, tid, burst_time, arrival_time=0):
        self.tid = tid
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

def fcfs(tasks):
    print("\n--- First Come First Serve (FCFS) ---")
    time = 0
    for task in sorted(tasks, key=lambda x: x.arrival_time):
        if time < task.arrival_time:
            time = task.arrival_time
        task.waiting_time = time - task.arrival_time
        time += task.burst_time
        task.completion_time = time
        task.turnaround_time = task.completion_time - task.arrival_time
        print(f"Task {task.tid}: Waiting={task.waiting_time}, Turnaround={task.turnaround_time}, Completion={task.completion_time}")

def sjf(tasks):
    print("\n--- Shortest Job First (SJF, Non-Preemptive) ---")
    time = 0
    completed = 0
    n = len(tasks)
    tasks_left = tasks[:]
    while completed < n:
        available = [t for t in tasks_left if t.arrival_time <= time]
        if not available:
            time += 1
            continue
        task = min(available, key=lambda x: x.burst_time)
        task.waiting_time = time - task.arrival_time
        time += task.burst_time
        task.completion_time = time
        task.turnaround_time = task.completion_time - task.arrival_time
        print(f"Task {task.tid}: Waiting={task.waiting_time}, Turnaround={task.turnaround_time}, Completion={task.completion_time}")
        tasks_left.remove(task)
        completed += 1

def round_robin(tasks, quantum):
    print(f"\n--- Round Robin (Quantum={quantum}) ---")
    time = 0
    queue = tasks[:]
    n = len(tasks)
    completed = 0
    while completed < n:
        for task in queue:
            if task.remaining_time > 0 and task.arrival_time <= time:
                exec_time = min(quantum, task.remaining_time)
                task.remaining_time -= exec_time
                time += exec_time
                if task.remaining_time == 0:
                    task.completion_time = time
                    task.turnaround_time = task.completion_time - task.arrival_time
                    task.waiting_time = task.turnaround_time - task.burst_time
                    print(f"Task {task.tid}: Waiting={task.waiting_time}, Turnaround={task.turnaround_time}, Completion={task.completion_time}")
                    completed += 1
            elif task.arrival_time > time:
                time = task.arrival_time

def main():
    num_tasks = int(input("Enter number of tasks: "))
    tasks = []
    for i in range(num_tasks):
        burst = int(input(f"Enter burst time for Task {i}: "))
        arrival = int(input(f"Enter arrival time for Task {i}: "))
        tasks.append(Task(i, burst, arrival))
    fcfs([Task(t.tid, t.burst_time, t.arrival_time) for t in tasks])
    sjf([Task(t.tid, t.burst_time, t.arrival_time) for t in tasks])
    quantum = int(input("Enter time quantum for Round Robin: "))
    round_robin([Task(t.tid, t.burst_time, t.arrival_time) for t in tasks], quantum)

if __name__ == "__main__":
    main()