### Table of Contents <br>
1. [WHAT IS MIQUALAT DATABASE](#WHAT-IS-MIQUALAT-DATABASE)
2. [INSTALL JUPYTER NOTEBOOK](#INSTALL-JUPYTER-NOTEBOOK)
3. [INSTALL MYSQL SERVER](#INSTALL-MYSQL-SERVER)
4. [INSTALL REQUIRED PYTHON LIBRARIES](#INSTALL-REQUIRED-PYTHON-LIBRARIES)
5. [DESCRIPTION OF THE FUNCTIONS FOLDER](#DESCRIPTION-OF-THE-FUNCTIONS-FOLDER)



3) INSTALL MYSQL SERVER
4) INSTALL MYSQLCLIENT
5) INSTALL REQUIRED LIBRARIES
6) DESCRIPTION OF THE FUNCTIONS FOLDER
7) DESCRIPTION OF THE OUTPUT FOLDER
8) MIQUALAT NOTEBOOK DESCRIPTION AND USE
9) CREATE BIOMART FILE
10) CREATE TABLE FILE
11) MIQUALAT DATABASE DESCRIPTION
12) DATABASE CHECK DESCRIPTION
13) AUTHORS


### WHAT IS MIQUALAT DATABASE
***
With Miqualat Notebooks you have access to an easy-to-use Jupyter Notebook interface. <br> 
Miqualat Notebook allows you to save data from publications, genes, variants, tecnique and other and associate them with descriptions and tags. <br> 
A control system has been implemented to maintain flexibility and freedom to import data while maintaining control over them. <br>
You can get this data from different databases as pubmed, ensembl, kegg and make automatically links. <br>
This relational database allows you to link and export information from different tables. <br>

### INSTALL JUPYTER NOTEBOOK
***
Update and upgrade your system (recommended). <br> 
$ sudo apt update && sudo apt upgrade <br> <br> 
Install python3-pip. <br> 
$ sudo apt install python3-pip <br>  <br> 
Install jupyter notebook. <br> 
$ sudo apt install jupyter-notebook <br> <br> 
If you need to configure the configuration file is located in /root/.jupyter/jupyter_notebook_config.py <br> 
$ jupyter-notebook --generate-config <br> <br> 
To access Jupyter Notebook you may need to set up a password. <br>
$ jupyter-notebook password <br><br> 
Run jupyter notebook (on port 8888 by default). <br> 
$ jupyter-notebook <br><br> 

### INSTALL MYSQL SERVER
***
Install apache2 and mysql-server. <br> 
$ sudo apt install apache2 <br>
$ sudo apt install mysql-server <br> <br> 
If you have a raspberry or similar system use this command to install mysql-server. <br> 
$ sudo apt install mariadb-server-10.0 <br> <br> 
Create user and set password for database (this user can be used to access in phpmyadmin, keep your credentials). <br> 
$ sudo mysql -u root <br>
$ CREATE USER 'user'@'localhost' IDENTIFIED BY 'password'; <br> <br> 
Grant privileges on all databases. <br> 
$ GRANT ALL PRIVILEGES ON * . * TO 'user'@'localhost'; <br> <br> 
Grant privileges on one databases (safer). <br>
$ GRANT ALL PRIVILEGES ON DATABASE. * TO 'user'@'localhost'; <br>
$ FLUSH PRIVILEGES; <br> <br> 
!! IMPORTANT (pay attention before continuing with the command below) !! <br>
!! When you install phpmyadmin (command below) after select apache2 (with TAB) and press SPACE !! <br>
!! After leave all empty (press ENTER) !! <br> 
$ sudo apt install phpmyadmin <br>
$ sudo systemctl restart apache2 <br> <br> 
Connect phpmyadmin using your browser (on port 80: /phpmyadmin). <br> 
http://server_ip(ex 192.168.0...)/phpmyadmin <br> <br> 
Show your IP. <br> 
$ hostname -I <br> <br> 
http://localhost/phpmyadmin (work only on local computer not for remote server) <br> 

### INSTALL MYSQLCLIENT
***
Install mysqlclient (connect database remotely using python). <br> 
Get more information at: https://pypi.org/project/mysqlclient/ <br> 
$ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential <br> 
$ pip3 install mysqlclient <br> <br> 
Update and upgrade your system (recommended). <br> 
$ sudo apt update && sudo apt upgrade <br> <br> 

### INSTALL REQUIRED PYTHON LIBRARIES
***
The following libraries are required for use miqualat notebooks. <br>
$ sudo pip3 install biopython <br>
$ sudo pip3 install ensembl-rest <br>
$ sudo pip3 install mygene <br><br>

### DESCRIPTION OF THE FUNCTIONS FOLDER
***
The functions in FUNCTIONS folder, contain python code that is recalled in the notebooks. <br><br>
1) ensembl_search.py <br>
Use the ensembl-rest library to get information about genes from the Ensembl database. <br><br>
2) ensembl_to_kegg_id.py <br>
Convert Ensembl gene id to the Kegg id of the gene and related pathways, using mygene and Bio.KEGG.REST (in biopython library). <br><br>
3) MIQUALAT_data_import_and_check.py <br>
Import and check the csv files processed with previous notebooks, using MySQLdb (in mysqlclient library). <br><br>
4) pubmed_search.py <br>
Carry out searches within the pubmed database using biopython. <br><br>
5) python_parser_biomart_gene_csv.py <br>
Convert the biomart file (which contains all biomart genes) into the right format for the GENE table. <br><br>

___________________________________________________________________________
DESCRIPTION OF THE OUTPUT FOLDER

In the OUTPUT folder are saved all the files processed by the notebook, to be imported into the miqualat database.

### MIQUALAT NOTEBOOKS DESCRIPTION AND USAGE
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
An error control system prevents the import of incorrect information, but import data into the database only when you are sure (racomanded). <br><br>
### LINK TO COMPLETE DOCUMENTATION
***
Click on the link to view the complete documentation. <br>

https://github.com/emanuele-tufarini/miqualat/blob/main/DOCUMENTATION.md <br>

___________________________________________________________________________
### CREATE BIOMART FILE
***
Go to https://www.ensembl.org/biomart/martview/afe982e758c87b06e672bc93a42a4f30.

Export  all results to File CSV.

Select dataset Ensembl Gene 101.

Select Species (refseq) (ex Cow genes (ARS-UCD1.2)).

Go to Attributes, Gene and create the biomart file following this header (select in the right order).

Gene stable ID,Gene name,Gene description,Chromosome/scaffold name,Gene start (bp),Gene end (bp),Strand

___________________________________________________________________________
### CREATE TABLE FILE
***
To pass the check the csv must have the following headers

!!
Create the Table file following this headers (create the header as it is written, do not add quotes or anything else).
!!

1) PUB_GEN_TEC_VAR_TAG TABLE 
integer_progressive_ID,pubmed_ID,ensembl_gene_ID,variant_name,tecnique,keyword_tags,relationship_note

2) PUBLICATION TABLE 
pubmed_ID,doi,article_title,article_authors,article_journal,publication_year

3) TECNIQUE TABLE 
tecnique,tecnique_short_description

4) TAG TABLE 
keyword_tags,tags_short_description

5) GENE TABLE 
ensembl_gene_ID,gene_name,gene_short_description,refseq,species,chromosome,start_coordinate,end_coordinate,strand

6) KEGG TABLE 
kegg_ID,kegg_object_type,kegg_object_name

7) GEN_KEGG TABLE 
ensembl_gene_ID,kegg_ID

8) VARIANT TABLE 
variant_name,variant_type,chromosome,chromosome_position,allele_reference,alternative_allele_reference

___________________________________________________________________________
### MIQUALAT DATABASE DESCRIPTION
***
Accesso a mysql server in localhost. <br><br>
mysql -u danilo -p <br>
Enter password: <br>
Welcome to the MySQL monitor.  Commands end with ; or \g. <br>
Your MySQL connection id is 15 <br>
Server version: 8.0.22-0ubuntu0.20.04.2 (Ubuntu) <br><br>
Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved. <br><br>
Oracle is a registered trademark of Oracle Corporation and/or its <br>
affiliates. Other names may be trademarks of their respective <br>
owners. <br><br>
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement. <br><br>
Importazione del file.sql nel quale è implementato il database. <br><br>
mysql> source MIQUALAT_create_database_and_tables.sql <br>
Query OK, 8 rows affected (0.08 sec) <br>
Query OK, 1 row affected (0.00 sec) <br>

Database changed <br>
Query OK, 0 rows affected, 2 warnings (0.03 sec) <br>

Query OK, 0 rows affected, 2 warnings (0.02 sec) <br>

Query OK, 0 rows affected, 1 warning (0.02 sec) <br>

Query OK, 0 rows affected (0.03 sec) <br>

Query OK, 0 rows affected (0.02 sec) <br>

Query OK, 0 rows affected (0.02 sec) <br>

Query OK, 0 rows affected, 1 warning (0.07 sec) <br>

Query OK, 0 rows affected (0.03 sec) <br><br>

Utilizzo del database MIQUALAT e visualizzazione delle tabelle. <br><br>
mysql> use MIQUALAT; <br>
Database changed <br>

mysql> SHOW TABLES; <br>
+---------------------+ <br>
| Tables_in_MIQUALAT  | <br>
+---------------------+ <br>
| GENE                | <br>
| GEN_KEGG            | <br>
| KEGG                | <br>
| PUBLICATION         | <br>
| PUB_GEN_VAR_TEC_TAG | <br>
| TAG                 | <br>
| TECNIQUE            | <br>
| VARIANT             | <br>
+---------------------+ <br>
8 rows in set (0.00 sec) <br><br>
Descrizione della struttura delle tabelle e del tipo di dato degli attributi di ogni entià e relazione. <br><br>

mysql> DESCRIBE GENE; <br>
+------------------------+--------------+------+-----+---------+-------+ <br>
| Field                  | Type         | Null | Key | Default | Extra | <br>
+------------------------+--------------+------+-----+---------+-------+ <br>
| ensembl_gene_ID        | varchar(20)  | NO   | PRI | NULL    |       | <br>
| gene_name              | varchar(20)  | YES  |     | NULL    |       | <br>
| gene_short_description | varchar(300) | YES  |     | NULL    |       | <br>
| refseq                 | varchar(50)  | NO   |     | NULL    |       | <br>
| species                | varchar(50)  | NO   |     | NULL    |       | <br>
| chromosome             | tinyint      | NO   |     | NULL    |       | <br>
| start_coordinate       | int unsigned | NO   |     | NULL    |       | <br>
| end_coordinate         | int unsigned | NO   |     | NULL    |       | <br>
| strand                 | tinyint      | NO   |     | NULL    |       | <br>
+------------------------+--------------+------+-----+---------+-------+ <br>
9 rows in set (0.00 sec) <br><br>

mysql> DESCRIBE GEN_KEGG; <br>
+-----------------+-------------+------+-----+---------+-------+ <br>
| Field           | Type        | Null | Key | Default | Extra | <br>
+-----------------+-------------+------+-----+---------+-------+ <br>
| ensembl_gene_ID | varchar(20) | NO   | PRI | NULL    |       | <br>
| kegg_ID         | varchar(20) | NO   | PRI | NULL    |       | <br>
+-----------------+-------------+------+-----+---------+-------+ <br>
2 rows in set (0.00 sec) <br> <br>

mysql> DESCRIBE KEGG; <br>
+------------------+--------------+------+-----+---------+-------+ <br>
| Field            | Type         | Null | Key | Default | Extra | <br>
+------------------+--------------+------+-----+---------+-------+ <br>
| kegg_ID          | varchar(20)  | NO   | PRI | NULL    |       | <br>
| kegg_object_type | varchar(30)  | NO   |     | NULL    |       | <br>
| kegg_object_name | varchar(300) | NO   |     | NULL    |       | <br>
+------------------+--------------+------+-----+---------+-------+ <br>
3 rows in set (0.00 sec) <br><br>

mysql> DESCRIBE PUBLICATION; <br>
+------------------+--------------+------+-----+---------+-------+ <br>
| Field            | Type         | Null | Key | Default | Extra | <br>
+------------------+--------------+------+-----+---------+-------+ <br>
| pubmed_ID        | int unsigned | NO   | PRI | NULL    |       | <br>
| article_title    | varchar(300) | NO   |     | NULL    |       | <br>
| article_authors  | varchar(300) | NO   |     | NULL    |       | <br>
| article_journal  | varchar(100) | NO   |     | NULL    |       | <br>
| publication_year | year         | NO   |     | NULL    |       | <br>
+------------------+--------------+------+-----+---------+-------+ <br>
5 rows in set (0.01 sec) <br><br>

mysql> DESCRIBE PUB_GEN_VAR_TEC_TAG; <br>
+------------------------+--------------+------+-----+---------+----------------+ <br>
| Field                  | Type         | Null | Key | Default | Extra          | <br>
+------------------------+--------------+------+-----+---------+----------------+ <br>
| integer_progressive_ID | int unsigned | NO   | PRI | NULL    | auto_increment | <br>
| pubmed_ID              | int unsigned | NO   | MUL | NULL    |                | <br>
| ensembl_gene_ID        | varchar(20)  | YES  | MUL | NULL    |                | <br>
| variant_name           | varchar(30)  | YES  | MUL | NULL    |                | <br>
| tecnique               | varchar(50)  | YES  | MUL | NULL    |                | <br>
| keyword_tags           | varchar(50)  | YES  | MUL | NULL    |                | <br>
| relationship_note      | varchar(200) | YES  |     | NULL    |                | <br>
+------------------------+--------------+------+-----+---------+----------------+ <br>
7 rows in set (0.01 sec) <br><br>

mysql> DESCRIBE TAG; <br>
+------------------------+--------------+------+-----+---------+-------+ <br>
| Field                  | Type         | Null | Key | Default | Extra | <br>
+------------------------+--------------+------+-----+---------+-------+ <br>
| keyword_tags           | varchar(50)  | NO   | PRI | NULL    |       | <br>
| tags_short_description | varchar(200) | NO   |     | NULL    |       | <br>
+------------------------+--------------+------+-----+---------+-------+ <br>
2 rows in set (0.01 sec) <br><br>

mysql> DESCRIBE TECNIQUE; <br>
+----------------------------+--------------+------+-----+---------+-------+ <br>
| Field                      | Type         | Null | Key | Default | Extra | <br>
+----------------------------+--------------+------+-----+---------+-------+ <br>
| tecnique                   | varchar(50)  | NO   | PRI | NULL    |       | <br>
| tecnique_short_description | varchar(300) | NO   |     | NULL    |       | <br>
+----------------------------+--------------+------+-----+---------+-------+ <br>
2 rows in set (0.01 sec) <br><br>

mysql> DESCRIBE VARIANT; <br>
+------------------------------+------------------+------+-----+---------+-------+ <br>
| Field                        | Type             | Null | Key | Default | Extra | <br>
+------------------------------+------------------+------+-----+---------+-------+ <br>
| variant_name                 | varchar(30)      | NO   | PRI | NULL    |       | <br>
| variant_type                 | varchar(30)      | NO   |     | NULL    |       | <br>
| chromosome                   | tinyint unsigned | NO   |     | NULL    |       | <br>
| chromosome_position          | int unsigned     | NO   |     | NULL    |       | <br>
| allele_reference             | varchar(50)      | NO   |     | NULL    |       | <br>
| alternative_allele_reference | varchar(50)      | NO   |     | NULL    |       | <br>
+------------------------------+------------------+------+-----+---------+-------+ <br>
6 rows in set (0.00 sec) <br><br>

SI TRATTA DI UN DATABASE RELAZIONALE <br>
*CON 6 TABELLE DI ENTITÀ{ <br>
											PUBLICATION, <br>
											GENE, <br>
											VARIANT, <br>
											TECNIQUE, <br>
											TAG, <br>
											KEGG <br>
}  <br>

*E 2 TABELLE RELAZIONALI{ <br>
											PUB_GEN_VAR_TEC_TAG, <br>
											GEN_KEGG <br>
} <br>

___________________________________________________________________________
DATABASE CHECK DESCRIPTION

1) entries fields number

2) entry duplicates

3) entries already present in the database

4) entry fields of a whole numerical nature

5) existence of foreign_keys for relational tables

6) special check for table PUB_GEN_VAR_TEC_TAG

7) special check for table GEN_KEGG

### LINK README
***
Click on the link to view the complete documentation. <br>

https://github.com/emanuele-tufarini/miqualat/blob/main/DOCUMENTATION.md <br>

Authors: Marco Milanesi, Danilo Pignotti, Emanuele Tufarini <br>
