##
# Programmer   : Regis Rodolfo Schuch
# Date         : 10 June 2024
#              : Applied Computing Research Group, Unijui University, Brazil
#              : regis.schuch@unijui.edu.br
#              :
# Title        : cheri-cap-experiment.py 
#              :
# Description  : The cheri-cap-experiment.py programme runs multiple instances of an executable programme called ./executable-program 
#              : until memory usage exceeds 90% of the total memory available on the system. It records the number of processes, the 
#              : amount of memory used and the elapsed time in a CSV file.
#              : Code breakdown:
#              : 1) Initialisation:
#              :  a) process_list: list to store the processes started.
#              :  b) max_memory_usage: gets the total amount of memory available on the system.
#              :  c) csv_file: name of the CSV file to save the results.
#              :  d) start_time: marks the start time to calculate the elapsed time.
#              : 2) Main Loop:
#              :  a) Start a New Process:
#              :   - Starts a new ./executable-program process using subprocess.Popen and adds it to the process_list.
#              :   - It waits 0.5 seconds to allow the process to allocate memory.
#              :  b) Check Memory Usage:
#              :   - Gets the amount of memory used (memory_used) using psutil.virtual_memory().used.
#              :   - Calculates the time elapsed (time_elapsed) since the start of execution, converting to milliseconds.
#              :   - Calculates the number of processes running (num_processes).
#              :   - Records this information in a CSV file.
#              :  c) Check if memory usage exceeds 90%:
#              :   - If memory usage exceeds 90% of the total available memory, the loop is interrupted.
#              :
# Install      :
# dependencies : The launcher.py code was executed on the Unix-enabled CheriBSD Operating System, which extends 
#              : FreeBSD
#              : $ sudo pkg64 install python3
#              :
# Compile and  :
# run          : $ python3 cheri-cap-experiment.py
#              :
#              :
##   

import subprocess
import psutil
import time
import csv

def main():
    process_list = []
    max_memory_usage = psutil.virtual_memory().total
    csv_file = 'cheri-cap-experiment-results.csv'
    start_time = time.time()

    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['Number of Processes', 'Memory Used (MB)', 'Time Elapsed (ms)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            # Start a new process
            #process = subprocess.Popen(['./integration_process'])
            process = subprocess.Popen(['env', 'LD_C18N_LIBRARY_PATH=.', './executable-program'])

            process_list.append(process)

            # Give some time for the process to start and allocate memory
            time.sleep(0.5)

            # Check memory usage
            memory_used = psutil.virtual_memory().used
            time_elapsed = (time.time() - start_time) * 1000  # Convert to milliseconds
            num_processes = len(process_list)
            
            writer.writerow({
                'Number of Processes': num_processes,
                'Memory Used (MB)': memory_used / (1024 * 1024),
                'Time Elapsed (ms)': time_elapsed
            })

            print(f'Processes: {num_processes}, Memory Used: {memory_used / (1024 * 1024):.2f} MB, Time Elapsed: {time_elapsed:.2f} ms')

            # Check if memory usage exceeds 90% of total memory
            if memory_used > max_memory_usage * 0.9:
                print("Memory usage exceeded 90% of total memory. Stopping...")
                break

        # Terminate all started processes
        for process in process_list:
            process.terminate()
            process.wait()

    print(f'Report saved to {csv_file}')

if __name__ == '__main__':
    main()
