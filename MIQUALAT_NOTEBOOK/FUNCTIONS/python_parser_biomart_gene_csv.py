'''
danilo pignotti
emanuele.tufarini@live.com
last modification 11-2020
'''

#import modules
import csv

def python_parser_biomart_gene_csv(biomart_file,refseq,species,chrom_autosomal,name,surname,data):
      
    # default value bos taurus
    if biomart_file == "":
        biomart_file = "/work/MIQUALAT_NOTEBOOK/INPUT/mart_export.csv"
    if species == "":
        species = "bos taurus"
    if chrom_autosomal == "":
        chrom_autosomal = "29"
        chrom_x = str(int(chrom_autosomal) + 1) 
        chrom_y = str(int(chrom_autosomal) + 2)    
        chrom_mt = str(int(chrom_autosomal) + 4)          
    if refseq == "":
        refseq = "ARS-UCD1.2"         

    with open(biomart_file,'r') as f:
        newlines = []
        for line in f.readlines():
            newlines.append(line.replace(';', '_'))
            
    # sostituisci i ";" con "_"
    with open(biomart_file, 'w') as f:
        for line in newlines:
            f.write(line)    

    scaffolds_count=0
    chromX_gene_count=0
    chromY_gene_count=0
    chromMT_gene_count=0
    bos_taurus_total_genes=0

    biomart_genes_file=open(biomart_file,"r")
    final_genes_file=open("./"+ name + "_" + surname +  str(data) + "_GENE.csv","w")
    csv_data=csv.reader(biomart_genes_file,delimiter=",")
    csv_writer=csv.writer(final_genes_file)

    header_gene_csv_file="ensembl_gene_ID,gene_name,gene_short_description,refseq,species,chromosome,start_coordinate,end_coordinate,strand"
    csv_writer.writerow(header_gene_csv_file.split(","))
    mart_export_header=next(csv_data)

    for i,line in enumerate(csv_data):
        bos_taurus_total_genes=i+1
        if(line[1] == ""):
            line[1]="NULL"
        if(line[2] == ""):
            line[2]="NULL"
        else:
            line[2]=line[2].split("[")[0]
        line.insert(3,refseq)
        line.insert(4,species)
        if(line[5] == "X"):
            chromX_gene_count+=1
            line[5]=chrom_x
        elif(line[5] == "Y"):
            chromY_gene_count+=1
            line[5]=chrom_y
        elif(line[5] == "MT"):
            chromMT_gene_count+=1
            line[5]=chrom_mt
        elif(len(line[5]) > 2):
            scaffolds_count+=1
            continue
        csv_writer.writerow(line)

    print("Bos_taurus total gene number: "+str(bos_taurus_total_genes))
    print("Bos_taurus total scaffold number: "+str(scaffolds_count))
    print("Bos_taurus gene number from autosomal and sexual chromosomes: "+str(bos_taurus_total_genes-scaffolds_count))
    print("Bos_taurus chromosome X gene number: "+str(chromX_gene_count))
    print("Bos_taurus chromosome Y gene number: "+str(chromY_gene_count))
    print("Bos_taurus chromosome MT gene number: "+str(chromMT_gene_count))