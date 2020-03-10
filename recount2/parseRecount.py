import json
import numpy as np
import pandas as pd

"""
parses tsv file using column headers as keys
"""
def parseTSV(path):
    dict = {}

    with open(path) as file:
        line_idx = 0
        for line in file:
            #get headers in a list
            if line_idx == 0:
                lsplit = line.split("\t")
                headers = [i.strip() for i in lsplit]
            #get each item in a dict with the index as the key
            if line_idx != 0:
                lsplit = line.split("\t")
                for item in lsplit:
                    #check if key exists
                    if lsplit.index(item) in dict:
                        dict[lsplit.index(item)].append(item.strip())
                    else:
                        dict[lsplit.index(item)] = []
            line_idx += 1
    return headers, dict

"""
parses column of tsv file
"""
def parseTSVCol(path, index):
    list = []

    with open(path) as file:
        line_idx = 0
        for line in file:
            if line_idx != 0:
                lsplit = line.split("\t")
                item = lsplit[index].strip()
                if item not in list:
                    list.append(item)
            line_idx += 1
    return list

"""
converts dict to json
"""
def toJson(path, dict):
    with open(path, 'w') as file:
        output = json.dumps(dict, indent=4)
        file.write(output)
        file.close()

#to get list of runs in order
#toJson("runs_in_order.json", parseTSVCol("SRP012682.tsv", 3))

#to get list of all genes
#toJson("gene_names.json", parseTSVCol("counts_gene.tsv", 9662))

#to get numpy array with rows as samples and columns as genes, each element is a count
df = pd.read_csv("counts_gene.tsv", sep="\t")
df.set_index("gene_id")
x = np.array(df)
np.save("recount2.npy", x.T)
