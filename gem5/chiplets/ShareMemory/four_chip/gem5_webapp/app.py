# app.py
from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/run_gem5', methods=['POST'])
def run_gem5():
    data = request.form
    cmd = f"{data['gem5Path']} {data['configPath']} --cmd=\"{data['cmd']}\" --cpu-type={data['cpuType']} --caches --mem-size={data['memSize']}GB --num-cpus {data['numCpus']} --chip_id '{data['chipId']}' --chip_num {data['chipNum']} --N {data['N']}"
    subprocess.run(cmd, shell=True)
    return "Simulation started"

if __name__ == '__main__':
    app.run(debug=True)

