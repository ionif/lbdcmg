#aionkov

"""
takes KinderMiner output csv and produces json file of struct:
"cell type": [genes]
"""
import csv
import json
import argparse

"""
parses cell markers db file
"""
def parseDB(path):
    cell_dict = {}

    with open(path) as file:
        line_idx = 0
        for line in file:
            if line_idx != 0:
                lsplit = line.split("\t")
                if lsplit[5] not in cell_dict:
                    cell_dict[lsplit[5]] = lsplit[7].split(", ")
                else:
                    for marker in lsplit[7].split(", "):
                        if marker not in cell_dict[lsplit[5]]:
                            cell_dict[lsplit[5]].append(marker)
            line_idx += 1
    return cell_dict

"""
parses KinderMiner csv output file
"""
def parseCSV(cell):
    gene_list = []
    path = cell + '.csv'
    with open(path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_idx = 0
        for row in csv_reader:
            if line_idx != 0:
                gene_list.append(row['target'])
            line_idx += 1
    
        return(gene_list)

"""
compares two json files
(one made with KM and the cell marker db)
"""
def cmp(path1, path2):
    with open(path1) as handle:
        one = json.loads(handle.read())
    with open(path2) as handle:
        two = json.loads(handle.read())

    #find common keys
    common_keys = one.keys() & two.keys()
    common_dict = {}
    for key in common_keys:
        common_values = list(set(one.get(key)) & set(two.get(key)))
        common_dict[key] = common_values
    
    fdict = {}
    #calculate ratio of common values / marker db vals
    #assumes the first path is the marker db path
    for key in common_dict:
        fdict[key] = len(common_dict.get(key))/len(one.get(key))
    return(fdict)

"""
converts dict to json
"""
def toJson(path, dict):
    with open(path, 'w') as file:
        output = json.dumps(dict, indent=4)
        file.write(output)
        file.close()

"""
main func
"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-db')
    parser.add_argument('-c', nargs='+')
    args = parser.parse_args()

    cell_types = ['T cell', 'B cell', 'natural killer cell']
    cell_dict = {}
    
    if not args.db and not args.c:
        for cell in cell_types:
            cell_dict[cell] = parseCSV(cell)

        toJson('output.json', cell_dict)
    #else the program is parsing the cell markers db
    elif not args.c:
        cell_dict = parseDB(args.db)
        toJson('markers.json', cell_dict)
    else:
        cell_dict = cmp(args.c[0], args.c[1])
        toJson('comparison.json', cell_dict)
if __name__ == "__main__":
    main()
