What is Miqualat Database
With Miqualat Notebooks you have access to an easy-to-use Jupyter Notebook interface.
Miqualat Notebook allows you to save data from publications, genes, variants, tecnique and other, associate them with descriptions and tags, import/export in the miqualat database.
A control system has been implemented to maintain flexibility and freedom to import data while maintaining control over them.
You can get this data from different databases as pubmed, ensembl, kegg and make automatically links.
This relational database allows you to link and export information from different tables.

Miqualat Notebooks Description and Usage
Notebooks are designed to simplify the generation, import, export of information from the database.
To use notebooks select the code cell and click on run, below will describe the notebooks and their functions.
Five notebooks have been built, that allow you to search, import and check into the miqualat database.

MIQUALAT_PUBLICATION_data_assess.ipynb
Carry out searches within the pubmed database, automatize data collection for PUBLICAITON table.
Creates PUBLICATION.csv file and move all searches (PUBMED_SEARCH_DATA_Y-m-d_H-M-S.txt format) in the OUTPUT folder.

MIQUALAT_DB_for_KEGG_data_assess.ipynb
Download genes and pathways from kegg database (from kegg code), automatize data collection for DB table.
Creates ALL_KEGG_GENE.csv (all kegg genes from kegg code) in the OUTPUT folder.
Creates ALL_KEGG_PATH.csv (all kegg pathways from kegg code) in the OUTPUT folder.

MIQUALAT_GENE_data_assess.ipynb
Allows you to download genes from ensembl database, automatize data collection for GENE table.
Option 1) get information from specific genes (ensembl gene id required).
Option 2) convert all genes downloaded from biomart (GENE.csv required).
In any case creates GENE.csv and move it in the OUTPUT folder.

MIQUALAT_GEN_DB_for_KEGG.ipynb
Correlates the ensembl gene id to the kegg id (if possible) of the gene and related pathway, automatize data collection for GEN_DB table.
Option 1) correlates the ensembl gene id to the kegg id of the gene and related pathways for specific gene (ensembl gene id required), for specific gene.
Option 2) processes the entire GENE.csv file.
Creates ENS_GENE_ID.csv (Ensembl gene id to Kegg gene id) in the OUTPUT folder.
Creates ENS_PATH_ID.csv (Ensembl gene id to Kegg pathways id) in the OUTPUT folder.

MIQUALAT_manual_table.ipynb
This notebook use the MIQUALAT_manual_table.py function in FUNCTIONS folder.
Allows you to create non-automated tables (PUB_GEN_TEC_VAR_TAG, TAG, TECNQUE, VARIANT). It’s based on loops who add one line at time at csv (when you enter yes the function repeat the loop or save file to the INPUT folder if you leave empty), there are an option to simplify this process and insert much genes at time to PUB_GEN_TEC_VAR_TAG table.
This function have a control on NULL value (convert all empty value in NULL if possible, in any case NULL is converted to uppercase). There are automatically warning if you cannot enter NULL value.
Follow the instructions to create the desired table.

MIQUALAT_data_import_and_check.ipynb
Allows the import of files processed with previous notebooks, once checked.
Input file are in INPUT folder folder. An error control system prevents the import of incorrect information, but import data into the database only when you are sure (racomanded).

MIQUALAT_gene_ontology_notebook.ipynb
Correlates the ensembl gene id or list of ensembl gene ids to all the gene ontology terms related to the ensembl ids in the entries list;
and creates the input files GEN_DB.csv and DB.csv to import gene ontology repository data in miqualat database. 

MIQUALAT_reactome_notebook.ipynb
Correlates the ensembl gene id or list of ensembl gene ids to all reactome pathway codes related to the ensembl ids in the entries list; 
and creates the input files GEN_DB.csv and DB.csv to import gene ontology repository data in miqualat database. 

MIQUALAT_data_export.ipynb
Allows you to export data from miqualat database.
To export the file enter the desired query number.
File are saved in OUTPUT folder with name table_TABLE_query_number_NUMBER_export_data_results__Y-m-d_h-d-s.

We proposed as variant_name this combination of values
international code for species/reference sequence (i.e. hg38 for last human reference sequence)
chromosome
position
reference allele
alternative allele (i.e. if the alternative allele is too long, try to find a way to summarize it)

example: hg38_1:146793_A|G

MIQUALAT_data_import_and_check.ipynb
Import checks types:
- headers check; 
- entry field number check;
- duplicate entry check;
- int data type field check;
- primary keys check;
- foreign keys check;
- NULL value field check;


















