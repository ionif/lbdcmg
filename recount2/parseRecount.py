import json
"""
parses tsv file
"""
def parseTSV(path, index):
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
toJson("runs_in_order.json", parseTSV("SRP012682.tsv", 3))

#to get list of all genes
toJson("gene_names.json", parseTSV("counts_gene.tsv", 9662))
