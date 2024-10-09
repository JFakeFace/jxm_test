import tkinter as tk
from tkinter import ttk
import subprocess

def run_gem5():
    command = f"{gem5_path.get()} {config_path.get()} "
    
    # 添加选中的 CPU 类型
    command += f"--cpu-type={cpu_type.get()} "
    
    if use_caches.get():
        command += "--caches "
    if use_l2.get():
        command += "--l2cache "
    with open('message0', 'w') as f:
        f.write('')
    command += f"--cmd=\"{cmd.get()}\" --mem-size={mem_size.get()}GB --num-cpus {num_cpus.get()} "
    command += f"--chip_id '{chip_id.get()}' --chip_num {chip_num.get()} --N {N.get()}"
    
    print("Running command:", command)
    subprocess.run(command, shell=True)

app = tk.Tk()
app.title("gem5 Configuration Interface")

# Define variables
gem5_path = tk.StringVar(value="../../../build/X86/gem5.opt")
config_path = tk.StringVar(value="../../../configs/deprecated/example/se.py")
cmd = tk.StringVar(value="./k0;./k1")
cpu_type = tk.StringVar()  # CPU 类型变量
mem_size = tk.StringVar(value="1")
num_cpus = tk.StringVar(value="2")
chip_id = tk.StringVar(value="0;1")
chip_num = tk.StringVar(value="2")
N = tk.StringVar(value="4")
use_caches = tk.BooleanVar(value=True)
use_l2 = tk.BooleanVar(value=False)

# Combobox for CPU type
cpu_options = ["DerivO3CPU", "MinorCPU", "AtomicSimpleCPU", "TimingSimpleCPU"]
ttk.Label(app, text="CPU Type:").grid(row=0, column=0, padx=5, pady=5)
cpu_type_combobox = ttk.Combobox(app, textvariable=cpu_type, values=cpu_options, state='readonly')
cpu_type_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
cpu_type_combobox.set(cpu_options[0])  # Default to the first option

# Function to add entry fields
def add_entry(label, variable, row):
    ttk.Label(app, text=label).grid(row=row, column=0, padx=5, pady=5)
    entry = ttk.Entry(app, textvariable=variable)
    entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

# Entries
add_entry("gem5 Path:", gem5_path, 1)
add_entry("Config Path:", config_path, 2)
add_entry("Command:", cmd, 3)
add_entry("Memory Size (GB):", mem_size, 4)
add_entry("Number of CPUs:", num_cpus, 5)
add_entry("Chip ID:", chip_id, 6)
add_entry("Number of Chips:", chip_num, 7)
add_entry("N:", N, 8)

# Checkbuttons
ttk.Checkbutton(app, text="Caches", variable=use_caches).grid(row=9, column=0, padx=5, pady=5, sticky='w')
ttk.Checkbutton(app, text="L2 Cache", variable=use_l2).grid(row=10, column=0, padx=5, pady=5, sticky='w')

# Run command button
ttk.Button(app, text="Run gem5", command=run_gem5).grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

app.mainloop()
import tkinter as tk
from tkinter import ttk
import subprocess

def run_gem5():
    command = f"{gem5_path.get()} {config_path.get()} "
    
    # 添加选中的 CPU 类型
    command += f"--cpu-type={cpu_type.get()} "
    
    if use_caches.get():
        command += "--caches "
    if use_l2.get():
        command += "--l2cache "
    with open('message0', 'w') as f:
        f.write('')
    command += f"--cmd=\"{cmd.get()}\" --mem-size={mem_size.get()}GB --num-cpus {num_cpus.get()} "
    command += f"--chip_id '{chip_id.get()}' --chip_num {chip_num.get()} --N {N.get()}"
    
    print("Running command:", command)
    subprocess.run(command, shell=True)

app = tk.Tk()
app.title("gem5 Configuration Interface")

# Define variables
gem5_path = tk.StringVar(value="../../../build/X86/gem5.opt")
config_path = tk.StringVar(value="../../../configs/deprecated/example/se.py")
cmd = tk.StringVar(value="./k0;./k1")
cpu_type = tk.StringVar()  # CPU 类型变量
mem_size = tk.StringVar(value="1")
num_cpus = tk.StringVar(value="2")
chip_id = tk.StringVar(value="0;1")
chip_num = tk.StringVar(value="2")
N = tk.StringVar(value="4")
use_caches = tk.BooleanVar(value=True)
use_l2 = tk.BooleanVar(value=False)

# Combobox for CPU type
cpu_options = ["DerivO3CPU", "MinorCPU", "AtomicSimpleCPU", "TimingSimpleCPU"]
ttk.Label(app, text="CPU Type:").grid(row=0, column=0, padx=5, pady=5)
cpu_type_combobox = ttk.Combobox(app, textvariable=cpu_type, values=cpu_options, state='readonly')
cpu_type_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
cpu_type_combobox.set(cpu_options[0])  # Default to the first option

# Function to add entry fields
def add_entry(label, variable, row):
    ttk.Label(app, text=label).grid(row=row, column=0, padx=5, pady=5)
    entry = ttk.Entry(app, textvariable=variable)
    entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')

# Entries
add_entry("gem5 Path:", gem5_path, 1)
add_entry("Config Path:", config_path, 2)
add_entry("Command:", cmd, 3)
add_entry("Memory Size (GB):", mem_size, 4)
add_entry("Number of CPUs:", num_cpus, 5)
add_entry("Chip ID:", chip_id, 6)
add_entry("Number of Chips:", chip_num, 7)
add_entry("N:", N, 8)

# Checkbuttons
ttk.Checkbutton(app, text="Caches", variable=use_caches).grid(row=9, column=0, padx=5, pady=5, sticky='w')
ttk.Checkbutton(app, text="L2 Cache", variable=use_l2).grid(row=10, column=0, padx=5, pady=5, sticky='w')

# Run command button
ttk.Button(app, text="Run gem5", command=run_gem5).grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

app.mainloop()

