### Table of Contents <br>
1. [WHAT IS MIQUALAT DATABASE](#WHAT-IS-MIQUALAT-DATABASE)
SET THE WORKING ENVIRONMENT
2) INSTALL JUPYTER NOTEBOOK
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

___________________________________________________________________________
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
Show your ip. <br> 
$ hostname -I <br> <br> 
http://localhost/phpmyadmin (work only on local computer not for remote server) <br> 

___________________________________________________________________________
INSTALL MYSQLCLIENT

Install mysqlclient (connect database remotely using python).

Get more information at: https://pypi.org/project/mysqlclient/

$ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

$ pip3 install mysqlclient

Update and upgrade your system (recommended).

$ sudo apt update && sudo apt upgrade

___________________________________________________________________________
INSTALL REQUIRED LIBRARIES

The following libraries are required for use miqualat notebooks

$ sudo pip3 install biopython 

$ sudo pip3 install ensembl-rest

$ sudo pip3 install mygene

___________________________________________________________________________
DESCRIPTION OF THE FUNCTIONS FOLDER

The functions in FUNCTIONS folder, contain python code that is recalled in the notebooks.

1) ensembl_search.py 

Use the ensembl-rest library to get information about genes from the Ensembl database.

2) ensembl_to_kegg_id.py 

Convert Ensembl gene id to the Kegg id of the gene and related pathways, using mygene and Bio.KEGG.REST (in biopython library).

3) MIQUALAT_data_import_and_check.py 

Import and check the csv files processed with previous notebooks, using MySQLdb (in mysqlclient library).

4) pubmed_search.py 

Carry out searches within the pubmed database using biopython.

5) python_parser_biomart_gene_csv.py 

Convert the biomart file (which contains all biomart genes) into the right format for the GENE table.

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
CREATE BIOMART FILE

Go to https://www.ensembl.org/biomart/martview/afe982e758c87b06e672bc93a42a4f30.

Export  all results to File CSV.

Select dataset Ensembl Gene 101.

Select Species (refseq) (ex Cow genes (ARS-UCD1.2)).

Go to Attributes, Gene and create the biomart file following this header (select in the right order).

Gene stable ID,Gene name,Gene description,Chromosome/scaffold name,Gene start (bp),Gene end (bp),Strand

___________________________________________________________________________
CREATE TABLE FILE

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
MIQUALAT DATABASE DESCRIPTION

##accesso a mysql server in localhost##
mysql -u danilo -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 15
Server version: 8.0.22-0ubuntu0.20.04.2 (Ubuntu)

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

##importazione del file.sql nel quale è implementato il database##
mysql> source MIQUALAT_create_database_and_tables.sql
Query OK, 8 rows affected (0.08 sec)

Query OK, 1 row affected (0.00 sec)

Database changed
Query OK, 0 rows affected, 2 warnings (0.03 sec)

Query OK, 0 rows affected, 2 warnings (0.02 sec)

Query OK, 0 rows affected, 1 warning (0.02 sec)

Query OK, 0 rows affected (0.03 sec)

Query OK, 0 rows affected (0.02 sec)

Query OK, 0 rows affected (0.02 sec)

Query OK, 0 rows affected, 1 warning (0.07 sec)

Query OK, 0 rows affected (0.03 sec)

##utilizzo del database MIQUALAT e visualizzazione delle tabelle##
mysql> use MIQUALAT;
Database changed
mysql> SHOW TABLES;
+---------------------+
| Tables_in_MIQUALAT  |
+---------------------+
| GENE                |
| GEN_KEGG            |
| KEGG                |
| PUBLICATION         |
| PUB_GEN_VAR_TEC_TAG |
| TAG                 |
| TECNIQUE            |
| VARIANT             |
+---------------------+
8 rows in set (0.00 sec)

##descrizione della struttura delle tabelle e del tipo di dato degli attributi di ogni entià e relazione##
mysql> DESCRIBE GENE;
+------------------------+--------------+------+-----+---------+-------+
| Field                  | Type         | Null | Key | Default | Extra |
+------------------------+--------------+------+-----+---------+-------+
| ensembl_gene_ID        | varchar(20)  | NO   | PRI | NULL    |       |
| gene_name              | varchar(20)  | YES  |     | NULL    |       |
| gene_short_description | varchar(300) | YES  |     | NULL    |       |
| refseq                 | varchar(50)  | NO   |     | NULL    |       |
| species                | varchar(50)  | NO   |     | NULL    |       |
| chromosome             | tinyint      | NO   |     | NULL    |       |
| start_coordinate       | int unsigned | NO   |     | NULL    |       |
| end_coordinate         | int unsigned | NO   |     | NULL    |       |
| strand                 | tinyint      | NO   |     | NULL    |       |
+------------------------+--------------+------+-----+---------+-------+
9 rows in set (0.00 sec)

mysql> DESCRIBE GEN_KEGG;
+-----------------+-------------+------+-----+---------+-------+
| Field           | Type        | Null | Key | Default | Extra |
+-----------------+-------------+------+-----+---------+-------+
| ensembl_gene_ID | varchar(20) | NO   | PRI | NULL    |       |
| kegg_ID         | varchar(20) | NO   | PRI | NULL    |       |
+-----------------+-------------+------+-----+---------+-------+
2 rows in set (0.00 sec)

mysql> DESCRIBE KEGG;
+------------------+--------------+------+-----+---------+-------+
| Field            | Type         | Null | Key | Default | Extra |
+------------------+--------------+------+-----+---------+-------+
| kegg_ID          | varchar(20)  | NO   | PRI | NULL    |       |
| kegg_object_type | varchar(30)  | NO   |     | NULL    |       |
| kegg_object_name | varchar(300) | NO   |     | NULL    |       |
+------------------+--------------+------+-----+---------+-------+
3 rows in set (0.00 sec)

mysql> DESCRIBE PUBLICATION;
+------------------+--------------+------+-----+---------+-------+
| Field            | Type         | Null | Key | Default | Extra |
+------------------+--------------+------+-----+---------+-------+
| pubmed_ID        | int unsigned | NO   | PRI | NULL    |       |
| article_title    | varchar(300) | NO   |     | NULL    |       |
| article_authors  | varchar(300) | NO   |     | NULL    |       |
| article_journal  | varchar(100) | NO   |     | NULL    |       |
| publication_year | year         | NO   |     | NULL    |       |
+------------------+--------------+------+-----+---------+-------+
5 rows in set (0.01 sec)

mysql> DESCRIBE PUB_GEN_VAR_TEC_TAG;
+------------------------+--------------+------+-----+---------+----------------+
| Field                  | Type         | Null | Key | Default | Extra          |
+------------------------+--------------+------+-----+---------+----------------+
| integer_progressive_ID | int unsigned | NO   | PRI | NULL    | auto_increment |
| pubmed_ID              | int unsigned | NO   | MUL | NULL    |                |
| ensembl_gene_ID        | varchar(20)  | YES  | MUL | NULL    |                |
| variant_name           | varchar(30)  | YES  | MUL | NULL    |                |
| tecnique               | varchar(50)  | YES  | MUL | NULL    |                |
| keyword_tags           | varchar(50)  | YES  | MUL | NULL    |                |
| relationship_note      | varchar(200) | YES  |     | NULL    |                |
+------------------------+--------------+------+-----+---------+----------------+
7 rows in set (0.01 sec)

mysql> DESCRIBE TAG;
+------------------------+--------------+------+-----+---------+-------+
| Field                  | Type         | Null | Key | Default | Extra |
+------------------------+--------------+------+-----+---------+-------+
| keyword_tags           | varchar(50)  | NO   | PRI | NULL    |       |
| tags_short_description | varchar(200) | NO   |     | NULL    |       |
+------------------------+--------------+------+-----+---------+-------+
2 rows in set (0.01 sec)

mysql> DESCRIBE TECNIQUE;
+----------------------------+--------------+------+-----+---------+-------+
| Field                      | Type         | Null | Key | Default | Extra |
+----------------------------+--------------+------+-----+---------+-------+
| tecnique                   | varchar(50)  | NO   | PRI | NULL    |       |
| tecnique_short_description | varchar(300) | NO   |     | NULL    |       |
+----------------------------+--------------+------+-----+---------+-------+
2 rows in set (0.01 sec)

mysql> DESCRIBE VARIANT;
+------------------------------+------------------+------+-----+---------+-------+
| Field                        | Type             | Null | Key | Default | Extra |
+------------------------------+------------------+------+-----+---------+-------+
| variant_name                 | varchar(30)      | NO   | PRI | NULL    |       |
| variant_type                 | varchar(30)      | NO   |     | NULL    |       |
| chromosome                   | tinyint unsigned | NO   |     | NULL    |       |
| chromosome_position          | int unsigned     | NO   |     | NULL    |       |
| allele_reference             | varchar(50)      | NO   |     | NULL    |       |
| alternative_allele_reference | varchar(50)      | NO   |     | NULL    |       |
+------------------------------+------------------+------+-----+---------+-------+
6 rows in set (0.00 sec)

##SI TRATTA DI UN DATABASE RELAZIONALE## 
*CON 6 TABELLE DI ENTITÀ{
											PUBLICATION,
											GENE,
											VARIANT,
											TECNIQUE,
											TAG,
											KEGG
} 

*E 2 TABELLE RELAZIONALI{
											PUB_GEN_VAR_TEC_TAG,
											GEN_KEGG
}

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
