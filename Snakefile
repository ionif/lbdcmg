rule all:
    input:
        "outputs/cx_output.json"

rule parse_CellMarker:
    input:
        "inputs/all_cell_markers.txt",
    output:
        "outputs/markers.json"
    shell:
        "python main.py -db {input} -o {output}"

rule parse_Kinderminer:
    input:
        "inputs/types.csv",
    output:
        "outputs/km_output.json"
    shell:
        "python main.py -o {output}"

rule compute_overlap:
    input:
        db = "outputs/markers.json",
        km = "outputs/km_output.json"
    output:
        "outputs/cx_output.json"
    shell:
        "python main.py -c {input.db} {input.km} -o {output}"

rule plot_overlap:
    input:
        
