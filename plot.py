import argparse
import os
import json 

parser = argparse.ArgumentParser()
parser.add_argument('-i')
args = parser.parse_args()

if args.i:
    in_path = args.i
else:
    in_path = "outputs/cx_output.json"

with open(in_path) as handle:
    data = json.loads(handle.read())
    
with open("gnuplot.dat", 'w') as f:
    for key, val in data.items():
        key = key.replace(" ", "-")
        f.write('%s\t %s\n' % (key, val))

os.system("gnuplot gnuplot.gp") 
