### Required Python Libraries
***
The following libraries are required for use miqualat notebooks. <br>
$ sudo pip3 install biopython <br>
$ sudo pip3 install ensembl-rest <br>
$ sudo pip3 install mygene <br>
$ sudo pip3 install pandas <br>

### What is Miqualat Database
***
With Miqualat Notebooks you have access to an easy-to-use Jupyter Notebook interface. <br> 
Miqualat Notebook allows you to save data from publications, genes, variants, tecnique and other, associate them with descriptions and tags, import/export in the miqualat database. <br> 
A control system has been implemented to maintain flexibility and freedom to import data while maintaining control over them. <br>
You can get this data from different databases as pubmed, ensembl, kegg and make automatically links. <br>
This relational database allows you to link and export information from different tables. <br>

### Miqualat Notebooks Description and Usage
***
Notebooks are designed to simplify the generation, import, export of information from the database. <br>
To use notebooks select the code cell and click on run, below will describe the notebooks and their functions. <br>
Five notebooks have been built, that allow you to search, import and check into the miqualat database. <br>
1) MIQUALAT_PUBLICATION_data_assess.ipynb <br>
Carry out searches within the pubmed database, automatize data collection for PUBLICAITON table. <br>
Creates PUBLICATION.csv file and move all searches (PUBMED_SEARCH_DATA_Y-m-d_H-M-S.txt format) in the OUTPUT folder. <br><br>
2) MIQUALAT_KEGG_data_assess.ipynb  <br>
Download genes and pathways from kegg database (from kegg <org> code), automatize data collection for KEGG table. <br>
Creates ALL_KEGG_GENE.csv (all kegg genes from <org> kegg code) in the OUTPUT folder. <br>
Creates ALL_KEGG_PATH.csv (all kegg pathways from <org> kegg code) in the OUTPUT folder. <br><br>
3) MIQUALAT_GENE_data_assess.ipynb  <br>
Allows you to download genes from ensembl database, automatize data collection for GENE table. <br>
Option 1) get information from specific genes (ensembl gene id required). <br>
Option 2) convert all genes downloaded from biomart (GENE.csv required). <br>
In any case  creates GENE.csv and move it in the OUTPUT folder. <br><br>
4) MIQUALAT_GEN_KEGG_data_assess.ipynb  <br>
Correlates the ensembl gene id to the kegg id (if possible) of the gene and related pathway, automatize data collection for GEN_KEGG table. <br>
Option 1) correlates the ensembl gene id to the kegg id of the gene and related pathways for specific gene (ensembl gene id required), for specific gene. <br>
Option 2) processes the entire GENE.csv file. <br>
Creates ENS_GENE_ID.csv (Ensembl gene id to Kegg gene id) in the OUTPUT folder. <br>
Creates ENS_PATH_ID.csv (Ensembl gene id to Kegg pathways id) in the OUTPUT folder. <br><br>
5) MIQUALAT_manual_table.ipynb <br>
This notebook use the MIQUALAT_manual_table.py function in FUNCTIONS folder. <br>
Allows you to create non-automated tables (PUB_GEN_TEC_VAR_TAG, TAG, TECNQUE, VARIANT). It’s based on loops who add one line at time at csv (when you enter yes the function repeat the loop or save file to the INPUT folder if you leave empty), there are an option to simplify this process and insert much genes at time to PUB_GEN_TEC_VAR_TAG table. <br>
This function have a control on NULL value (convert all empty value in NULL if possible, in any case NULL is converted to uppercase). There are automatically warning if you cannot enter NULL value. <br>
Follow the instructions to create the desired table. <br><br>
6) MIQUALAT_data_import_and_check.ipynb  <br>
Allows the import of files processed with previous notebooks, once checked. <br>
Input file are in INPUT folder folder.
An error control system prevents the import of incorrect information, but import data into the database only when you are sure (racomanded). <br><br>
7) MIQUALAT_data_export.ipynb                        
Allows you to export data from miqualat database. <br>
To export the file enter the desired query number. <br>
File are saved in OUTPUT folder with name table_TABLE_query_number_NUMBER_export_data_results__Y-m-d_h-d-s. <br><br>
We proposed as variant_name this combination of values <br>
1. international code for species/reference sequence (i.e. hg38 for last human reference sequence) <br> 
2. chromosome  <br>
3. position  <br>
4. reference allele  <br>
5. alternative allele (i.e. if the alternative allele is too long, try to find a way to summarize it) <br><br>
example: hg38_1:146793_A|G <br> <br>

### LINK TO COMPLETE DOCUMENTATION
***
Click on the link to view the complete documentation. <br>

https://github.com/emanuele-tufarini/miqualat/blob/main/miqualat_documentation.pdf <br>

Authors: Marco Milanesi, Danilo Pignotti, Emanuele Tufarini <br>
