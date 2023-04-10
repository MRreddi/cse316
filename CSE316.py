from queue import Queue

class Process:
    def __init__(self, pid, burst_time, arrival_time, priority):
        self.pid = pid
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.priority = priority
        self.remaining_time = burst_time

    def __lt__(self, other):
        return self.priority < other.priority

class Scheduler:
    def __init__(self, quantum):
        self.level1_queue = Queue()
        self.level2_queue = Queue()
        self.quantum = quantum

    def add_process(self, pid, burst_time, arrival_time, priority):
        process = Process(pid, burst_time, arrival_time, priority)
        self.level1_queue.put(process)

    def run(self):
        current_time = 0
        while not self.level1_queue.empty() or not self.level2_queue.empty():

            if not self.level1_queue.empty():
                process = self.level1_queue.get()

                if not self.level1_queue.empty() and (self.level1_queue.queue[0]<process):

                    self.level2_queue.put(process)
                else:

                    time_slice = min(process.remaining_time, 2)
                    process.remaining_time -= time_slice
                    current_time += time_slice

                    if process.remaining_time == 0:
                        print(f"Process {process.pid} finished at time {current_time}")
                    else:

                        process.priority -= 1
                        self.level1_queue.put(process)

            elif not self.level2_queue.empty():
                process = self.level2_queue.get()
                time_slice = min(process.remaining_time, self.quantum)
                process.remaining_time -= time_slice
                current_time += time_slice

                if process.remaining_time == 0:
                    print(f"Process {process.pid} finished at time {current_time}")
                else:
                    self.level2_queue.put(process)


quantum = int(input("Enter time quantum for round-robin scheduling: "))


n = int(input("Enter the number of processes: "))
scheduler = Scheduler(quantum)
for i in range(n):
    pid = i+1
    burst_time = int(input(f"Enter the burst time for process {pid}: "))
    arrival_time = int(input(f"Enter the arrival time for process {pid}: "))
    priority = int(input(f"Enter the priority for process {pid}: "))
    scheduler.add_process(pid, burst_time, arrival_time, priority)


scheduler.run()
