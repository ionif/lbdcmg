rule cm_db:
    input:
        "inputs/all_cell_markers.txt",
    output:
        "outputs/markers.json"
    shell:
        "python main.py -db {input} -o {output}"

rule km:
    input:
        "inputs/km.txt",
    output:
        "outputs/km_output.json"
    shell:
        "python main.py -o {output}"

rule cx:
    input:
        db = "outputs/markers.json"
        km = "outputs/output.json"
    output:
        "outputs/cx_output.json"
    shell:
        "python main.py -c {input.db} {input.km} -o {output}"
