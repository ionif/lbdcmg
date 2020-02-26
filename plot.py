import argparse
import os
import json 

with open("outputs/cx_output.json") as handle:
    data = json.loads(handle.read())
    
with open("gnuplot.dat", 'w') as f:
    for key, val in data.items():
        key = key.replace(" ", "-")
        f.write('%s\t %s\n' % (key, val))

os.system("gnuplot gnuplot.gp") 
