### What is Miqualat Database
***
With Miqualat Notebooks you have access to an easy-to-use Jupyter Notebook interface. <br> 
Miqualat Notebook allows you to save data from publications, genes, variants, tecnique and other and associate them with descriptions and tags. <br> 
A control system has been implemented to maintain flexibility and freedom to import data while maintaining control over them. <br>
You can get this data from different databases as pubmed, ensembl, kegg and make automatically links. <br>
This relational database allows you to link and export information from different tables. <br>
### Miqualat Notebooks Description and Usage
***
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
5) MIQUALAT_data_import_and_check.ipynb  <br>
Allows the import of files processed with previous notebooks, once checked. <br>
Input file are in INPUT folder folder.
An error control system prevents the import of incorrect information, but import data into the database only when you are sure (racomanded). <br><br>
6) MIQUALAT_data_export.ipynb  <br>                          
Allows you to export data from miqualat database. <br>
To export the file enter the desired query number.
File are saved in OUTPUT folder with name table_TABLE_query_number_NUMBER_export_data_results__Y-m-d_h-d-s. <br><br>
  
### LINK TO COMPLETE DOCUMENTATION
***
Click on the link to view the complete documentation. <br>

https://github.com/emanuele-tufarini/miqualat/blob/main/miqualat_documentation.pdf <br>

Authors: Marco Milanesi, Danilo Pignotti, Emanuele Tufarini <br>
