import os
import subprocess

def get_pids(process_name):
    try:
        pids = subprocess.check_output(["pgrep", "-f", process_name]).decode().strip().splitlines()
        return [int(pid) for pid in pids]
    except subprocess.CalledProcessError:
        print(f"Process '{process_name}' not found.")
        return []

def get_memory_addresses(pid):
    try:
        procstat_output = subprocess.check_output(["procstat", "-v", str(pid)]).decode().splitlines()
        rw_regions = []
        for line in procstat_output:
            if 'rw-' in line:  
                parts = line.split()
                start_addr = int(parts[1], 16)
                end_addr = int(parts[2], 16)
                rw_regions.append((start_addr, end_addr))
        if not rw_regions:
            print("No RW memory regions found.")
        return rw_regions
    except subprocess.CalledProcessError as e:
        print(f"Error obtaining memory information for PID {pid}: {e}")
        return []

def scrape_memory(pid, rw_regions, label):
    if pid is None or not rw_regions:
        print("Memory scraping cannot proceed due to insufficient information.")
        return
    
    try:
        with open(f"/proc/{pid}/mem", "rb") as mem_file:
            for start, end in rw_regions:
                mem_file.seek(start)
                buffer = mem_file.read(end - start)
                print(f"Data read from {label} memory (from 0x{start:x} to 0x{end:x}):")
                print(buffer.decode(errors='replace'))  
    except OSError as e:
        print(f"Error accessing process memory: {e}")

if __name__ == "__main__":    
    process_names = ["main_program"]
    
    for i, process_name in enumerate(process_names):
        pids = get_pids(process_name)
        
        if not pids:
            print(f"No PIDs found for {process_name}")
            continue
        
        for pid in pids:
            rw_regions = get_memory_addresses(pid)
            if rw_regions:
                scrape_memory(pid, rw_regions, process_name)
