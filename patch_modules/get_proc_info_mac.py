import os
import psutil
import time
import pandas as pd
import matplotlib.pyplot as plt

def capture_cpu_usage(interval, csv_file_name):
    # Initial capture of CPU times
    initial_cpu_times = {p.pid: p.cpu_times() for p in psutil.process_iter() if p.pid != 0 and p.status() != psutil.STATUS_ZOMBIE}
    # Wait for the interval
    time.sleep(interval)
    # Final capture of CPU times
    final_cpu_times = {p.pid: p.cpu_times() for p in psutil.process_iter() if p.pid != 0 and p.status() != psutil.STATUS_ZOMBIE}

    # Log PIDs of zombie processes
    zombie_processes = [p.pid for p in psutil.process_iter() if p.status() == psutil.STATUS_ZOMBIE]
    if zombie_processes:
        print(f"Zombie Processes: {zombie_processes}")

    # Calculate CPU usage
    cpu_usage_data = []
    for pid, final_times in final_cpu_times.items():
        if pid in initial_cpu_times:
            initial_times = initial_cpu_times[pid]
            cpu_time_diff = sum(f - i for f, i in zip(final_times, initial_times))
            cpu_usage_data.append((pid, psutil.Process(pid).name(), cpu_time_diff / interval * 100))

    # Save to CSV
    df = pd.DataFrame(cpu_usage_data, columns=['PID', 'Process Name', 'CPU Usage (%)'])
    df.sort_values(by='CPU Usage (%)', ascending=False, inplace=True)
    df.head(10).to_csv(csv_file_name, index=False)

def plot_cpu_usage_from_csv(csv_file_name):
    # Read the CSV file
    df = pd.read_csv(csv_file_name)
    
    # Plotting
    plt.figure(figsize=(10, 8))
    bars = plt.barh(df['Process Name'], df['CPU Usage (%)'], color='skyblue')
    plt.xlabel('CPU Usage (%)')
    plt.title('Top 10 Processes by CPU Usage')

    # Annotate each bar
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height() / 2, f'{width:.2f}%', ha='left', va='center')

    plt.show()

def plot_mac_cpu_usage_from_csv():
     # Path for the new directory
    notes_directory_path = '.notes'

    # Check if the directory already exists
    if not os.path.exists(notes_directory_path):
        # Create the directory
        os.makedirs(notes_directory_path)
        print(f"Directory '{notes_directory_path}' was created.")
    else:
        print(f"Directory '{notes_directory_path}' already exists.")

    csv_file_name = '.notes/mac_top_processes_by_cpu_usage.csv'
    interval = 10  # Interval in seconds
    # Capture CPU usage and save to CSV
    capture_cpu_usage(interval, csv_file_name)
    # Plot the CPU usage data from the CSV file
    plot_cpu_usage_from_csv(csv_file_name)
