import pandas as pd
import numpy as np
import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

# User-configurable thresholds (modify as needed)
cpu_threshold = 90  # Percentage
memory_threshold = 90  # Percentage
storage_threshold = 90  # Percentage
network_threshold = 1000000  # Network I/O in Bytes

# Initializing empty lists to store data for plotting
time_points = []
cpu_percentage = []
memory_percentage = []
network_io_sent = []
network_io_received = []
storage_utilization = []

# Initialize a DataFrame to store data for the table
data = pd.DataFrame(columns=["Time", "CPU Utilization (%)", "Memory Utilization (%)", "Network Sent (Bytes)", "Network Received (Bytes)", "Storage Utilization (%)"])

# Create a figure for plotting
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Virtual Machine Monitoring System', fontsize=16)

# Function to update data for plotting and table
def update_data(_):
    # Getting current time
    current_time = datetime.now()
    time_points.append(current_time)

    # Getting CPU utilization
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_percentage.append(cpu_percent)

    # Getting memory utilization
    memory = psutil.virtual_memory()
    memory_percentage.append(memory.percent)

    # Getting Network I/O
    network_io = psutil.net_io_counters()
    network_io_sent.append(network_io.bytes_sent)
    network_io_received.append(network_io.bytes_recv)

    # Getting Storage utilization (default C:drive)
    storage = psutil.disk_usage('/')
    storage_utilization.append(storage.percent)

    # Alerting logic (unchanged)
    if cpu_percent > cpu_threshold:
        print("High CPU Usage Alert", f"CPU usage is {cpu_percent}%.")
    if memory.percent > memory_threshold:
        print("High Memory Usage Alert", f"Memory usage is {memory.percent}%.")
    if storage.percent > storage_threshold:
        print("High Storage Usage Alert", f"Storage usage is {storage.percent}%.")
    if network_io.bytes_sent > network_threshold:
        print("High Network Usage Alert", f"Network I/O sent: {network_io.bytes_sent} bytes.")

    # Limiting data points to the last 50 units for better visualization
    if len(time_points) > 50:
        time_points.pop(0)
        cpu_percentage.pop(0)
        memory_percentage.pop(0)
        network_io_sent.pop(0)
        network_io_received.pop(0)
        storage_utilization.pop(0)

    # Update the DataFrame for the table
    data.loc[current_time] = [current_time, cpu_percent, memory.percent, network_io.bytes_sent, network_io.bytes_recv, storage.percent]

    # Clear subplots and plot data (unchanged)
    for ax in axs.flat:
        ax.clear()

    axs[0, 0].plot(time_points, cpu_percentage, label='CPU Utilization (%)')
    axs[0, 0].set_title('CPU Utilization')

    axs[0, 1].plot(time_points, memory_percentage, label='Memory Utilization (%)')
    axs[0, 1].set_title('Memory Utilization')

    axs[1, 0].plot(time_points, network_io_sent, label='Network Sent/Input (in Bytes)')
    axs[1, 0].plot(time_points, network_io_received, label='Network Received/Output (in Bytes)')
    axs[1, 0].set_title('Network I/O Utilization')

    axs[1, 1].plot(time_points, storage_utilization, label='Storage Utilization (%)')
    axs[1, 1].set_title('Storage Utilization')

    for ax in axs.flat:
        ax.legend(loc='upper right')

# Creating an animation for dynamic visualization
ani = FuncAnimation(fig, update_data, interval=1000, save_count=len(time_points), cache_frame_data=False)

# Display the table and conclusions
def display_table_and_conclusions():
    # Display the data table
    print("Data Table:")
    print(data.to_string(index=False, justify='left'))

    # Analyze the data and provide conclusions with prevention measures
    # Example: If memory utilization is above the threshold, suggest stopping or optimizing memory-intensive processes
    max_memory_utilization = data["Memory Utilization (%)"].max()
    if max_memory_utilization > memory_threshold:
        print("\nHigh Memory Utilization Detected.")
        print(f"Maximum Memory Utilization: {max_memory_utilization}%")
        print("Suggested Prevention Measure: Stop or optimize memory-intensive processes.")

# Display the table and conclusions once the animation has run for a while
ani.event_source.stop()
update_data(None)  # Run one final data update
display_table_and_conclusions()

plt.tight_layout()
plt.show()
