rule cm_db:
    input:
        "inputs/all_cell_markers.txt",
    output:
        "outputs/markers.json"
    shell:
        "python main.py -db {input} | samtools view -Sb - > {output}"
