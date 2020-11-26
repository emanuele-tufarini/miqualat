DROP DATABASE IF EXISTS MIQUALAT;
CREATE DATABASE MIQUALAT;
USE MIQUALAT;

CREATE TABLE PUBLICATION (
	pubmed_ID INT (8) UNSIGNED NOT NULL,
	doi VARCHAR (100),
	article_title VARCHAR (300) NOT NULL,
	article_authors VARCHAR (300) NOT NULL,
	article_journal VARCHAR (100) NOT NULL,
	publication_year YEAR (4) NOT NULL,
	PRIMARY KEY (pubmed_ID)
);

CREATE TABLE GENE (
	ensembl_gene_ID VARCHAR (20) NOT NULL,
	gene_name VARCHAR (20),
	gene_short_description VARCHAR (300),
	refseq VARCHAR (50) NOT NULL,
	species VARCHAR (50) NOT NULL,
	chromosome TINYINT (2) NOT NULL,
	start_coordinate INT UNSIGNED NOT NULL,
	end_coordinate INT UNSIGNED NOT NULL,
	strand TINYINT (2) NOT NULL,
	PRIMARY KEY (ensembl_gene_ID)
);

CREATE TABLE VARIANT (
	variant_name VARCHAR (30) NOT NULL,
	variant_type VARCHAR (30) NOT NULL,
	chromosome  TINYINT (2) UNSIGNED NOT NULL,
	chromosome_position INT UNSIGNED NOT NULL,
	allele_reference VARCHAR (50) NOT NULL,
	alternative_allele_reference VARCHAR (50) NOT NULL,
	PRIMARY KEY (variant_name)
);

CREATE TABLE TECNIQUE (
	tecnique VARCHAR (50) NOT NULL,
	tecnique_short_description VARCHAR (300) NOT NULL,
	PRIMARY KEY (tecnique)
);

CREATE TABLE TAG (
	keyword_tags VARCHAR (50) NOT NULL,
	tags_short_description VARCHAR (200) NOT NULL,
	PRIMARY KEY (keyword_tags)
);

CREATE TABLE KEGG (
	kegg_ID VARCHAR (20) NOT NULL,
	kegg_object_type VARCHAR (30) NOT NULL,
	kegg_object_name VARCHAR (300) NOT NULL,
	PRIMARY KEY (kegg_ID)
);

CREATE TABLE PUB_GEN_VAR_TEC_TAG (
	integer_progressive_ID INT UNSIGNED NOT NULL AUTO_INCREMENT,
	pubmed_ID INT (8) UNSIGNED NOT NULL,
	ensembl_gene_ID VARCHAR (20),
	variant_name VARCHAR (30) ,
	tecnique VARCHAR (50),
	keyword_tags VARCHAR (50),
	relationship_note VARCHAR (200),
	PRIMARY KEY (integer_progressive_ID),
	FOREIGN KEY (pubmed_ID) REFERENCES PUBLICATION (pubmed_ID),
	FOREIGN KEY (ensembl_gene_ID) REFERENCES GENE (ensembl_gene_ID),
	FOREIGN KEY (variant_name) REFERENCES VARIANT (variant_name),
	FOREIGN KEY (tecnique) REFERENCES TECNIQUE (tecnique),
	FOREIGN KEY (keyword_tags) REFERENCES TAG (keyword_tags)
);

CREATE TABLE GEN_KEGG (
	ensembl_gene_ID VARCHAR (20) NOT NULL,
	kegg_ID VARCHAR (20) NOT NULL,
	PRIMARY KEY (ensembl_gene_ID, kegg_ID),
	FOREIGN KEY (ensembl_gene_ID) REFERENCES GENE (ensembl_gene_ID),
	FOREIGN KEY (kegg_ID) REFERENCES KEGG (kegg_ID)
);
