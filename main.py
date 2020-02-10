#aionkov

"""
takes KinderMiner output csv and produces json file of struct:
"cell type": [genes]
"""
import csv
import json

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
    cell_types = ['T-cell', 'B-cell', 'natural-killer-cell']
    cell_dict = {}

    for cell in cell_types:
        cell_dict[cell] = parseCSV(cell)

    toJson('output.json', cell_dict)

if __name__ == "__main__":
    #parseCSV('results')
    main()
