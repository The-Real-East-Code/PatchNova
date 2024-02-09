import os
import psutil
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt

# Function to get process CPU times at the start or end of the interval
def get_process_cpu_times():
    process_cpu_times = {}
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            cpu_times = proc.cpu_times()
            process_cpu_times[proc.info['pid']] = (proc.info['name'], cpu_times)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_cpu_times

# Function to calculate CPU usage percentages for processes
def calculate_cpu_percentages(start_times, end_times, interval, total_cpu_time):
    cpu_percentages = {}
    for pid, end_time in end_times.items():
        if pid in start_times:
            # Calculate the CPU time spent by the process during the interval
            cpu_time_diff = sum([e - s for s, e in zip(start_times[pid][1], end_time[1])])
            # Calculate the CPU usage percentage
            cpu_percentage = (cpu_time_diff / total_cpu_time) * 100
            cpu_percentages[pid] = (end_time[0], cpu_percentage)
    return cpu_percentages


def get_win_proc_by_cpu_percentage():
    interval = 10  # Sampling interval in seconds
    total_cpus = psutil.cpu_count()
    
    # Get the total CPU time available during the interval
    total_cpu_time = total_cpus * interval
    
    # Get initial CPU times of processes
    start_cpu_times = get_process_cpu_times()
    
    # Wait for the specified interval
    time.sleep(interval)
    
    # Get final CPU times of processes
    end_cpu_times = get_process_cpu_times()
    
    # Calculate CPU usage percentages
    cpu_percentages = calculate_cpu_percentages(start_cpu_times, end_cpu_times, interval, total_cpu_time)
    
    # Sort processes by CPU usage and prepare the data for the CSV
    top_processes = sorted(cpu_percentages.items(), key=lambda x: x[1][1], reverse=True)[:10]
    
    # Write to CSV file

    # Path for the new directory
    notes_directory_path = '.notes'

    # Check if the directory already exists
    if not os.path.exists(notes_directory_path):
        # Create the directory
        os.makedirs(notes_directory_path)
        print(f"Directory '{notes_directory_path}' was created.")
    else:
        print(f"Directory '{notes_directory_path}' already exists.")

    csv_file_name = '.notes\\_Win_processes_by_cpu_usage.csv'
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Process Name", "PID", "CPU Usage (%)"])
        for pid, (name, cpu_usage) in top_processes:
            writer.writerow([name, pid, f"{cpu_usage:.2f}"])

    print(f"Top 10 processes by CPU usage (%) have been written to {csv_file_name}")


def plot_win_cpu_usage_from_csv():
    get_win_proc_by_cpu_percentage()
    csv_file_name = '.notes\\_Win_processes_by_cpu_usage.csv'
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_name)
    # Sort the DataFrame by CPU Usage in descending order
    df_sorted = df.sort_values(by='CPU Usage (%)', ascending=True)
    # Plotting
    plt.figure(figsize=(10, 8))
    bars = plt.barh(df_sorted['Process Name'], df_sorted['CPU Usage (%)'], color='skyblue')
    # Annotate each bar with the value of CPU usage
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2, f'{width:.2f}%', ha='left', va='center')
    
    plt.xlabel('CPU Usage (%)')
    plt.title('Top 10 Processes by CPU Usage')
    plt.show()
