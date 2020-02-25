import argparse
import os

with open("outputs/cx_output.json") as handle:
    data = json.loads(handle.read())
    
with open("gnuplot.dat", 'w') as f:
    for key, val in data.items():
        f.write('%s\t %s' % (key, val))

os.system("gnuplot gnuplot.gp") 
