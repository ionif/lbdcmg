#aionkov

"""
takes KinderMiner output csv and produces json file of struct:
"cell type": [genes]
"""
import csv
import json
import argparse

def parseTypes(path):
    gene_list = []
    with open(path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_idx = 0
        for row in csv_reader:
            gene_list.append(row['type'])
        return(gene_list)

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
    gene_dict = {}
    path = cell + '.csv'
    try:
        with open(path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_idx = 0
            for row in csv_reader:
                if line_idx != 0:
                    gene_dict[row['target']] = row['p_value']
                line_idx += 1
    except:
        print("File: " + path + " does not exist.")

    return(gene_dict)

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
        two_val = two.get(key)
#        print(two_val.keys())
        common_values = list(set(one.get(key)) & set(two_val.keys()))
        print(common_values)
        common_dict[key] = common_values
    
    fdict = {}
    #calculate ratio of common values / marker db vals
    #assumes the first path is the marker db path
    for key in common_dict:
        fdict[key] = len(common_dict.get(key))/len(one.get(key))
    return(fdict)

"""
find difference in keys for one dict versus another
"""
def diffDict(path1, path2):
    with open(path1) as handle:
        one = json.loads(handle.read())
    with open(path2) as handle:
        two = json.loads(handle.read())

    #find common keys
    common_keys = one.keys() & two.keys()
    common_dict = {}

    #diff lists
    not_in_one = []
    not_in_two = []

    for key in common_keys:
        for item in one.get(key):
            if item not in two.get(key):
                not_in_two.append(item)
        for item in two.get(key):
            if item not in one.get(key):
                not_in_one.append(item)
        #value for each cell type
        value_dict = {}
        value_dict["KM_not_CM"] = not_in_one
        value_dict["CM_not_KM"] = not_in_two
        
        #map cell type to val
        common_dict[key] = value_dict

    return(common_dict)

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
    parser.add_argument('-d', nargs='+')
    parser.add_argument('-o')
    args = parser.parse_args()

#    cell_types = ['T cell', 'B cell', 'natural killer cell']
    cell_dict = {}
    out_path = 'output.json'
    if args.o:
        out_path = args.o

    if not args.db and not args.c and not args.d:
        #search for types.csv which holds list of all types to parse
        cell_types = parseTypes("inputs/types.csv")
        print(cell_types)
        for cell in cell_types:
            path = "inputs/" + str(cell)
            data = parseCSV(path)
            #check if list is not empty
            if data:
                cell = cell.split("/")
                cell = cell[len(cell)-1]
                cell_dict[cell] = data
        toJson(out_path, cell_dict)
    #else the program is parsing the cell markers db
    elif not args.c and not args.d:
        cell_dict = parseDB(args.db)
        toJson(out_path, cell_dict)
    elif not args.d:
        cell_dict = cmp(args.c[0], args.c[1])
        toJson(out_path, cell_dict)
    else:
        cell_dict = diffDict(args.d[0], args.d[1])
        toJson(out_path, cell_dict)

if __name__ == "__main__":
    main()
