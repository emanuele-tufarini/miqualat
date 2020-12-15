#importazione del modulo pandas per la rappresentazione in forma di dataframe dei risultati delle queries sul database e per la creazione dei file in formato .csv di export dal database, importazione del metodo display dal module IPython.display per il print a schermo sotto forma di dataframe dei risultati delle queries effettuate sul database, del modulo MySQLdb per connettersi al DATABASE MIQUALAT, della libreria getpass dalla quale viene usato il modulo getpass per mascherare la password di accesso al database server, del modulo datetime per gestire l'identificazione dei file di export output attraverso il filename#
import pandas as pd
from IPython.display import display
import MySQLdb
import getpass
import datetime

#definizione della funzione di export dei dati dal database MIQUALAT#
def miqualat_db_data_exporter():
    
    #variabili richieste come parametri di input all'utente: database username e password#
    user=input("enter your username: ")
    pswd=getpass.getpass("enter your password: ")
    
    #CONNESSIONE AL SERVER DOVE È ALLOCATO IL DATABASE#
    mydb=MySQLdb.connect(host="localhost", user=user, passwd=pswd, db="MIQUALAT")
    cursor=mydb.cursor()
    
    #variabile che alloca la data di esecuzione per rinominare il filename di export output#
    date=datetime.datetime.now()
    
    #definizione di una variabile locale di tipo dizionario per la selezione delle tabelle su cui operare l'export dei dati dal database MIQUALAT#
    table_dict={
    "1":"GENE",
    "2":"KEGG",
    "3":"GEN_KEGG",
    "4":"PUBLICATION",
    "5":"TECNIQUE",
    "6":"TAG",
    "7":"VARIANT",
    "8":"PUB_GEN_VAR_TEC_TAG"
    }
    
    #print del menu a tendina di selezione delle tabelle da cui effettuare l'export dei dati#
    print("\ntables selection menu from which to export data:\n")
    for key in table_dict.keys():
        print("enter "+key+" to export data from database MIQUALAT following table: "+table_dict[key]+";")

    #variabili richieste come parametri di input all'utente: tabelle selezionate per l''export dal database#
    selection=input("\nenter tables selection numbers (i.e. 7 or 1,2,3): ")
    
    #definizione di una variabile locale di tipo lista per allocare il nome delle tabelle risultato della selezione di input da parte dell'utente#
    selected_tables=[]
    
    #check della selezione digitata come parametro di input dall'utente#
    if(len(selection) == 0):
        print("\nWARNING: please enter a selection code in range 1-8")
    elif(len(selection) == 1):
        if(selection in table_dict.keys()):
            selected_tables.append(table_dict[selection])
        else:
            print("\nWARNING: the inserted code: "+selection+" is not present in the tables selection menu")
    else:
        for code in selection.split(","):
            if(code in table_dict.keys()):
                selected_tables.append(table_dict[code])
            else:
                print("\nWARNING: the inserted code: "+code+" is not present in the tables selection menu")
                
    #INIZIO DELLA FASE DI ESPORTAZIONE DEI DATI DOPO LA FASE DI RACCOLTA DELLA SELEZIONE#
    #definizione di una variabile locale di tipo dizionario per l'allocazione degli attributi/fields di ogni tabella del db MIQUALAT#
    field_dictionary={
    "GENE":["ensembl_gene_ID","gene_name","gene_short_description","refseq","species","chromosome","start_coordinate","end_coordinate","strand"],
    "KEGG":["kegg_ID","kegg_object_type","kegg_object_name"],
    "GEN_KEGG":["ensembl_gene_ID","kegg_ID"],
    "PUBLICATION":["pubmed_ID","doi","article_title","article_authors","article_journal","publication_year"],
    "TECNIQUE":["tecnique","tecnique_short_description"],
    "TAG":["keyword_tags","tags_short_description"],
    "VARIANT":["variant_name","variant_type","chromosome","position","reference_allele","alternative_allele","rs_ID","species","refseq"],
    "PUB_GEN_VAR_TEC_TAG":["integer_progressive_ID","pubmed_ID","ensembl_gene_ID","variant_name","tecnique","keyword_tags","relationship_note"],
    }
    
    #allocazione in una variabile locale di una stringa per la richiesta del salvataggio dell'output dell'estrazione tramite queries in un file .csv#
    save_file_string="\nafter displayed exportation example do you want to save results in a .csv file in OUTPUT folder? (i.e. yes or not): "
    
    #iterazione sui table names selezionati in input dall'utente#
    for table_name in selected_tables:
        
        #SELEZIONE DELLE QUERIES SPECIFICHE PER TABELLA#
        
        #menu di selezione come parametro di input delle queries specifiche per la tabella GENE#
        if(table_name == "GENE"):
            print(
                    "\nqueires selection menu to export data from table GENE:\n",
                    "\n1: to extract all table records;",
                    "\n2: to extract specific record relative to an input ensembl ID;",
                    "\n3: to extract specific record relative to an input gene_name;",
                    "\n4: to extract all the species and relative refseq version;",
                    "\n5: to count genes total numbers sorted by species;",
                    "\n6: to extract all genes from an input species;",
                    "\n7: to extract all genes located on an input chromosome for an input species;",
                    "\n8: to extract all genes located between start and end input coordinates on an input chromosome for an input species;"
            )
        
            #variabili richieste come parametri di input all'utente: queries selezionate per l'export dalla tabella GENE del database MIQUALAT#
            gene_query_selection=input("\nenter GENE table queries selection numbers (i.e. 4 or 1,2,3): ")
            
            #dizionario delle queries specifiche per la tabella GENE#
            gene_queries={
                                    "1":"SELECT * FROM GENE;",
                                    "2":"SELECT * FROM GENE WHERE GENE.ensembl_gene_ID=\'%s\';",
                                    "3":"SELECT * FROM GENE WHERE GENE.gene_name=\'%s\';",
                                    "4":"SELECT GENE.species,GENE.refseq FROM GENE GROUP BY GENE.species,GENE.refseq;",
                                    "5":"SELECT GENE.species,COUNT(*) FROM GENE GROUP BY GENE.species;",
                                    "6":"SELECT * FROM GENE WHERE GENE.species=\'%s\';",
                                    "7":"SELECT * FROM GENE WHERE GENE.chromosome=%s AND GENE.species=\'%s\';",
                                    "8":"SELECT * FROM GENE WHERE GENE.chromosome=%s AND GENE.species=\'%s\' AND GENE.start_coordinate>=%s AND GENE.end_coordinate<=%s;"
            }
        
            #esecuzione sul database delle queries selezionate in input dall'utente per l'export dei dati dalla tabella GENE#
            for code in gene_query_selection.split(","):
                
                #allocazione di una variabile di tipo stringa per memorizzare il path dinamico di salvataggio del file .csv di export dalle varie tabelle#
                save_file_path="./OUTPUT/table_"+table_name+"_query_number_"+str(code)+"_export_data_results_"+ str(date.year)+"-"+str(date.month)+"-"+str(date.day)+"_"+str(int(date.hour))+"-"+str(date.minute)+"-"+str(date.second)+".csv"
                
                if(code == "1"):
                    result_header=field_dictionary["GENE"]
                    cursor.execute(gene_queries[code])
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "2"):
                    result_header=field_dictionary["GENE"]
                    ensembl_gene_ID_list=input("\nenter ensembl_gene_ID (i.e. ENSBTAG00000000009 or ENSBTAG00000000010,ENSBTAG00000000011,ENSBTAG00000000012,...): ").split(",")
                    IDs_query_results=[]
                    for ID in ensembl_gene_ID_list:
                        cursor.execute(gene_queries[code] % ID)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            IDs_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=IDs_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "3"):
                    result_header=field_dictionary["GENE"]
                    gene_name_list=input("\nenter gene_name (i.e. UBL7 or UBL7,TDH,TTC33,...): ").split(",")
                    gene_names_query_results=[]
                    for gene_name in gene_name_list:
                        cursor.execute(gene_queries[code] % gene_name)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            gene_names_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=gene_names_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "4"):
                    result_header=[field_dictionary["GENE"][4],field_dictionary["GENE"][3]]
                    cursor.execute(gene_queries[code])
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf="./OUTPUT/table_"+table_name+"_query_number_"+str(code)+"_export_data_results_" + str(date.year)+"-"+str(date.month)+"-"+str(date.day)+"_"+str(int(date.hour))+"-"+str(date.minute)+"-"+str(date.second)+".csv",sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "5"):
                    result_header=[field_dictionary["GENE"][4],"COUNT(genes)"]
                    cursor.execute(gene_queries[code])
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "6"):
                    result_header=field_dictionary["GENE"]
                    cursor.execute(gene_queries[code] % input("\nenter species (i.e. Bos taurus or Homo sapiens): "))
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "7"):
                    result_header=field_dictionary["GENE"]
                    cursor.execute(gene_queries[code] % (input("\nenter chromosome: "),input("\nenter species: ")))
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "8"):
                    result_header=field_dictionary["GENE"]
                    cursor.execute(gene_queries[code] % (input("\nenter chromosome: "),input("\nenter species: "),input("\nenter start_coordinate: "),input("\nenter end_coordinate: ")))
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
               
        #menu di selezione come parametro di input delle queries specifiche per la tabella PUB_GEN_VAR_TEC_TAG#
        if(table_name == "PUB_GEN_VAR_TEC_TAG"):
            print(
                    "\nqueires selection menu to export data from table PUB_GEN_VAR_TEC_TAG:\n",
                    "\n1: to extract all table records;",
                    "\n2: to extract pubmed_ID,doi,article_title of all publications related to an input ensembl_gene_ID;",
                    "\n3: to extract pubmed_ID,doi,article_title of all publications related to an input gene_name;",
                    "\n4: to extract ensembl_gene_ID and gene_name of all genes related to an input pubmed_ID;",
                    "\n5: to extract ensembl_gene_ID and gene_name of all genes related to an input doi;",
                    "\n6: to extract pubmed_ID,doi,article_title and ensembl_gene_ID and gene_name of all publications and genes related to an input keyword_tag;",
                    "\n7: to extract ensembl_gene_ID and gene_name of all genes related to an input variant_name;",
                    "\n8: to extract all tecnique informations of all tecniques related to an input pubmed_ID;",
                    "\n9: to extract all kegg_ID informations of all kegg_IDs (gene, pathway, protein, enzyme...etc.) related to an input pubmed_ID;",
                    "\n10: to extract pubmed_ID,doi,article_title,ensembl_gene_ID and gene_name of all publications and genes related to an input kegg_ID (kegg code of gene, pathway, protein, enzyme...etc.);",
                    "\n11: to extract pubmed_ID,doi,article_title,ensembl_gene_ID and gene_name of all publications and genes related to an input compound name to search into kegg_object_name;",
                    "\n12: to extract all record fields and gene_name related to an input pubmed_ID;",
                    "\n13: to extract all record fields and gene_name related to an input doi;",
                    "\n14: to extract pubmed_ID,doi,article_title and tecnique_name and keyword_tag related to an input ensembl_gene_ID;",
                    "\n15: to extract pubmed_ID,doi,article_title and tecnique_name and keyword_tag related to an input gene_name;"
            )
        
            #variabili richieste come parametri di input all'utente: queries selezionate per l'export dalla tabella PUB_GEN_VAR_TEC_TAG del database MIQUALAT#
            pub_gen_var_tec_tag_query_selection=input("\nenter PUB_GEN_VAR_TEC_TAG table queries selection numbers (i.e. 4 or 1,2,3): ")
            
            #dizionario delle queries specifiche per la tabella PUB_GEN_VAR_TEC_TAG#
            pub_gen_var_tec_tag_queries={
                                                            "1":"SELECT * FROM PUB_GEN_VAR_TEC_TAG;",
                                                            "2":"SELECT DISTINCT PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID,PUBLICATION.pubmed_ID,PUBLICATION.doi,PUBLICATION.article_title FROM PUB_GEN_VAR_TEC_TAG,PUBLICATION WHERE PUB_GEN_VAR_TEC_TAG.pubmed_ID=PUBLICATION.pubmed_ID AND PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID=\'%s\';",
                                                            "3":"SELECT DISTINCT GENE.gene_name,PUBLICATION.pubmed_ID,PUBLICATION.doi,PUBLICATION.article_title FROM GENE,PUB_GEN_VAR_TEC_TAG,PUBLICATION WHERE GENE.ensembl_gene_ID=PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID AND PUB_GEN_VAR_TEC_TAG.pubmed_ID=PUBLICATION.pubmed_ID AND GENE.gene_name=\'%s\';",
                                                            "4":"SELECT DISTINCT PUB_GEN_VAR_TEC_TAG.pubmed_ID,PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID,GENE.gene_name FROM PUB_GEN_VAR_TEC_TAG,GENE WHERE PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID=GENE.ensembl_gene_ID AND PUB_GEN_VAR_TEC_TAG.pubmed_ID=%s;",
                                                            "5":"SELECT DISTINCT PUBLICATION.doi,PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID,GENE.gene_name FROM PUBLICATION,PUB_GEN_VAR_TEC_TAG,GENE WHERE PUBLICATION.pubmed_ID=PUB_GEN_VAR_TEC_TAG.pubmed_ID AND PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID=GENE.ensembl_gene_ID AND PUBLICATION.doi=\'%s\';",
                                                            "6":"SELECT DISTINCT PUB_GEN_VAR_TEC_TAG.keyword_tags,PUB_GEN_VAR_TEC_TAG.pubmed_ID,PUBLICATION.doi,PUBLICATION.article_title,PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID,GENE.gene_name FROM PUBLICATION,PUB_GEN_VAR_TEC_TAG,GENE WHERE PUBLICATION.pubmed_ID=PUB_GEN_VAR_TEC_TAG.pubmed_ID AND PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID=GENE.ensembl_gene_ID AND PUB_GEN_VAR_TEC_TAG.keyword_tags=\'%s\';",
                                                            "7":"SELECT DISTINCT PUB_GEN_VAR_TEC_TAG.variant_name,PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID,GENE.gene_name FROM PUB_GEN_VAR_TEC_TAG,GENE WHERE PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID=GENE.ensembl_gene_ID AND PUB_GEN_VAR_TEC_TAG.variant_name=\'%s\';",
                                                            "8":"SELECT DISTINCT PUB_GEN_VAR_TEC_TAG.pubmed_ID,PUB_GEN_VAR_TEC_TAG.tecnique,TECNIQUE.tecnique_short_description FROM PUB_GEN_VAR_TEC_TAG,TECNIQUE WHERE PUB_GEN_VAR_TEC_TAG.tecnique=TECNIQUE.tecnique AND PUB_GEN_VAR_TEC_TAG.pubmed_ID=%s;",
                                                            "9":"SELECT DISTINCT PUB_GEN_VAR_TEC_TAG.pubmed_ID,GEN_KEGG.kegg_ID,KEGG.kegg_object_type,KEGG.kegg_object_name FROM PUB_GEN_VAR_TEC_TAG,GENE,GEN_KEGG,KEGG WHERE PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID=GENE.ensembl_gene_ID AND GENE.ensembl_gene_ID=GEN_KEGG.ensembl_gene_ID AND GEN_KEGG.kegg_ID=KEGG.kegg_ID AND PUB_GEN_VAR_TEC_TAG.pubmed_ID=%s;",
                                                            "10":"SELECT DISTINCT GEN_KEGG.kegg_ID,GEN_KEGG.ensembl_gene_ID,GENE.gene_name,PUB_GEN_VAR_TEC_TAG.pubmed_ID,PUBLICATION.doi,PUBLICATION.article_title FROM GEN_KEGG,GENE,PUB_GEN_VAR_TEC_TAG,PUBLICATION WHERE GEN_KEGG.ensembl_gene_ID=GENE.ensembl_gene_ID AND GENE.ensembl_gene_ID=PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID AND PUB_GEN_VAR_TEC_TAG.pubmed_ID=PUBLICATION.pubmed_ID AND GEN_KEGG.kegg_ID=\'%s\';",
                                                            "11":"SELECT DISTINCT KEGG.kegg_object_name,GEN_KEGG.ensembl_gene_ID,GENE.gene_name,PUB_GEN_VAR_TEC_TAG.pubmed_ID,PUBLICATION.doi,PUBLICATION.article_title FROM KEGG,GEN_KEGG,GENE,PUB_GEN_VAR_TEC_TAG,PUBLICATION WHERE KEGG.kegg_ID=GEN_KEGG.kegg_ID AND GEN_KEGG.ensembl_gene_ID=GENE.ensembl_gene_ID AND GENE.ensembl_gene_ID=PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID AND PUB_GEN_VAR_TEC_TAG.pubmed_ID=PUBLICATION.pubmed_ID AND KEGG.kegg_object_name LIKE \'%%%s%%\';",
                                                            "12":"SELECT PUB_GEN_VAR_TEC_TAG.pubmed_ID,PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID,GENE.gene_name,PUB_GEN_VAR_TEC_TAG.variant_name,PUB_GEN_VAR_TEC_TAG.tecnique,PUB_GEN_VAR_TEC_TAG.keyword_tags,PUB_GEN_VAR_TEC_TAG.relationship_note FROM PUB_GEN_VAR_TEC_TAG,GENE WHERE PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID=GENE.ensembl_gene_ID AND PUB_GEN_VAR_TEC_TAG.pubmed_ID=%s;",
                                                            "13":"SELECT PUBLICATION.doi,PUB_GEN_VAR_TEC_TAG.pubmed_ID,PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID,GENE.gene_name,PUB_GEN_VAR_TEC_TAG.variant_name,PUB_GEN_VAR_TEC_TAG.tecnique,PUB_GEN_VAR_TEC_TAG.keyword_tags,PUB_GEN_VAR_TEC_TAG.relationship_note FROM PUBLICATION,PUB_GEN_VAR_TEC_TAG,GENE WHERE PUBLICATION.pubmed_ID=PUB_GEN_VAR_TEC_TAG.pubmed_ID AND PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID=GENE.ensembl_gene_ID AND PUBLICATION.doi=\'%s\';",
                                                            "14":"SELECT PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID,PUB_GEN_VAR_TEC_TAG.pubmed_ID,PUBLICATION.doi,PUBLICATION.article_title,PUB_GEN_VAR_TEC_TAG.tecnique,PUB_GEN_VAR_TEC_TAG.keyword_tags FROM PUB_GEN_VAR_TEC_TAG,PUBLICATION WHERE PUB_GEN_VAR_TEC_TAG.pubmed_ID=PUBLICATION.pubmed_ID AND PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID=\'%s\';",
                                                            "15":"SELECT GENE.gene_name,PUB_GEN_VAR_TEC_TAG.pubmed_ID,PUBLICATION.doi,PUBLICATION.article_title,PUB_GEN_VAR_TEC_TAG.tecnique,PUB_GEN_VAR_TEC_TAG.keyword_tags FROM GENE,PUB_GEN_VAR_TEC_TAG,PUBLICATION WHERE GENE.ensembl_gene_ID=PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID AND PUB_GEN_VAR_TEC_TAG.pubmed_ID=PUBLICATION.pubmed_ID AND GENE.gene_name=\'%s\'"
            }
            
            #esecuzione sul database delle queries selezionate in input dall'utente per l'export dei dati dalla tabella PUB_GEN_VAR_TEC_TAG#
            for code in pub_gen_var_tec_tag_query_selection.split(","):
                
                #allocazione di una variabile di tipo stringa per memorizzare il path dinamico di salvataggio del file .csv di export dalle varie tabelle#
                save_file_path="./OUTPUT/table_"+table_name+"_query_number_"+str(code)+"_export_data_results_"+ str(date.year)+"-"+str(date.month)+"-"+str(date.day)+"_"+str(int(date.hour))+"-"+str(date.minute)+"-"+str(date.second)+".csv"
                
                if(code == "1"):
                    result_header=field_dictionary["PUB_GEN_VAR_TEC_TAG"]
                    cursor.execute(pub_gen_var_tec_tag_queries[code])
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "2"):
                    result_header=["ensembl_gene_ID","pubmed_ID","doi","article_title"]
                    ensembl_gene_ID_list=input("\nenter ensembl_gene_ID (i.e. ENSBTAG00000000009 or ENSBTAG00000000010,ENSBTAG00000000011,ENSBTAG00000000012,...): ").split(",")
                    IDs_query_results=[]
                    for ID in ensembl_gene_ID_list:
                        cursor.execute(pub_gen_var_tec_tag_queries[code] % ID)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            IDs_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=IDs_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "3"):
                    result_header=["gene_name","pubmed_ID","doi","article_title"]
                    gene_name_list=input("\nenter gene_name (i.e. UBL7 or UBL7,TDH,TTC33,...): ").split(",")
                    gene_names_query_results=[]
                    for gene_name in gene_name_list:
                        cursor.execute(pub_gen_var_tec_tag_queries[code] % gene_name)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            gene_names_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=gene_names_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "4"):
                    result_header=["pubmed_ID","ensembl_gene_ID","gene_name"]
                    pubmed_ID_list=input("\nenter pubmed_ID (i.e. 29024632 or 29024632,29024999,...): ").split(",")
                    pubmed_ID_query_results=[]
                    for pubmed_ID in pubmed_ID_list:
                        cursor.execute(pub_gen_var_tec_tag_queries[code] % pubmed_ID)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            pubmed_ID_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=pubmed_ID_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "5"):
                    result_header=["doi","ensembl_gene_ID","gene_name"]
                    doi_list=input("\nenter doi (i.e. 10.1016/j.bbrc.2017.10.038 or 10.1016/j.bbrc.2017.10.038,10.1016/j.bbrc.2017.10.999,...): ").split(",")
                    doi_query_results=[]
                    for doi in doi_list:
                        cursor.execute(pub_gen_var_tec_tag_queries[code] % doi)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            doi_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=doi_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "6"):
                    result_header=["keyword_tags","pubmed_ID","doi","article_title","ensembl_gene_ID","gene_name"]
                    keyword_tags_list=input("\nenter keyword_tags (i.e. glutathione or glutathione,mammary gland,peak lactation,...): ").split(",")
                    keyword_tags_query_results=[]
                    for keyword_tag in keyword_tags_list:
                        cursor.execute(pub_gen_var_tec_tag_queries[code] % keyword_tag)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            keyword_tags_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=keyword_tags_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "7"):
                    result_header=["variant_name","ensembl_gene_ID","gene_name"]
                    variant_name_list=input("\nenter variant_name (i.e. A or A,G,T,C): ").split(",")
                    variant_name_query_results=[]
                    for variant_name in variant_name_list:
                        cursor.execute(pub_gen_var_tec_tag_queries[code] % variant_name)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            variant_name_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=variant_name_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "8"):
                    result_header=["pubmed_ID","tecnique","tecnique_short_description"]
                    pubmed_ID_list=input("\nenter pubmed_ID (i.e. 29024632 or 29024632,29024999,...): ").split(",")
                    pubmed_ID_query_results=[]
                    for pubmed_ID in pubmed_ID_list:
                        cursor.execute(pub_gen_var_tec_tag_queries[code] % pubmed_ID)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            pubmed_ID_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=pubmed_ID_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "9"):
                    result_header=["pubmed_ID","kegg_ID","kegg_object_type","kegg_object_name"]
                    pubmed_ID_list=input("\nenter pubmed_ID (i.e. 29024632 or 29024632,29024999,...): ").split(",")
                    pubmed_ID_query_results=[]
                    for pubmed_ID in pubmed_ID_list:
                        cursor.execute(pub_gen_var_tec_tag_queries[code] % pubmed_ID)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            pubmed_ID_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=pubmed_ID_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "10"):
                    result_header=["kegg_ID","ensembl_gene_ID","gene_name","pubmed_ID","doi","article_title"]
                    kegg_ID_list=input("\nenter kegg_ID (kegg code of gene, pathway, protein, enzyme...etc.)(i.e. bta:281495 or bta:281495,bta:281210,bta:615507,...): ").split(",")
                    kegg_ID_query_results=[]
                    for kegg_ID in kegg_ID_list:
                        cursor.execute(pub_gen_var_tec_tag_queries[code] % kegg_ID)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            kegg_ID_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=kegg_ID_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "11"):
                    result_header=["kegg_object_name","ensembl_gene_ID","gene_name","pubmed_ID","doi","article_title"]
                    kegg_obj_name_list=input("\nenter compound name to search into kegg_object_name (i.e. glutathione or glutathione,other molecules name): ").split(",")
                    kegg_obj_name_query_results=[]
                    for kegg_obj_name in kegg_obj_name_list:
                        cursor.execute(pub_gen_var_tec_tag_queries[code] % kegg_obj_name)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            kegg_obj_name_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=kegg_obj_name_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "12"):
                    result_header=["pubmed_ID","ensembl_gene_ID","gene_name","variant_name","tecnique","keyword_tags","relationship_note"]
                    pubmed_ID_list=input("\nenter pubmed_ID (i.e. 29024632 or 29024632,29024999,...): ").split(",")
                    pubmed_ID_query_results=[]
                    for pubmed_ID in pubmed_ID_list:
                        cursor.execute(pub_gen_var_tec_tag_queries[code] % pubmed_ID)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            pubmed_ID_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=pubmed_ID_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL") 
                elif(code == "13"):
                    result_header=["doi","pubmed_ID","ensembl_gene_ID","gene_name","variant_name","tecnique","keyword_tags","relationship_note"]
                    doi_list=input("\nenter doi (i.e. 10.1016/j.bbrc.2017.10.038 or 10.1016/j.bbrc.2017.10.038,10.1016/j.bbrc.2017.10.999,...): ").split(",")
                    doi_query_results=[]
                    for doi in doi_list:
                        cursor.execute(pub_gen_var_tec_tag_queries[code] % doi)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            doi_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=doi_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "14"):
                    result_header=["ensembl_gene_ID","pubmed_ID","doi","article_title","tecnique","keyword_tags"]
                    ensembl_gene_ID_list=input("\nenter ensembl_gene_ID (i.e. ENSBTAG00000000009 or ENSBTAG00000000010,ENSBTAG00000000011,ENSBTAG00000000012,...): ").split(",")
                    IDs_query_results=[]
                    for ID in ensembl_gene_ID_list:
                        cursor.execute(pub_gen_var_tec_tag_queries[code] % ID)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            IDs_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=IDs_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "15"):
                    result_header=["gene_name","pubmed_ID","doi","article_title","tecnique","keyword_tags"]
                    gene_name_list=input("\nenter gene_name (i.e. UBL7 or UBL7,TDH,TTC33,...): ").split(",")
                    gene_names_query_results=[]
                    for gene_name in gene_name_list:
                        cursor.execute(pub_gen_var_tec_tag_queries[code] % gene_name)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            gene_names_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=gene_names_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                        
        #menu di selezione come parametro di input delle queries specifiche per la tabella TECNIQUE#
        if(table_name == "TECNIQUE"):
            print(
                    "\nqueires selection menu to export data from table TECNIQUE:\n",
                    "\n1: to extract all table records;",
                    "\n2: to extract all record fields relative to an input tecnique;",
                    "\n3: to extract all record fields relative to an input term to search into field tecnique_short_description;"
                    )
                    
            #variabili richieste come parametri di input all'utente: queries selezionate per l'export dalla tabella TECNIQUE del database MIQUALAT#
            tecnique_query_selection=input("\nenter TECNIQUE table queries selection numbers (i.e. 4 or 1,2,3): ")
            
            #dizionario delle queries specifiche per la tabella TECNIQUE#
            tecnique_queries={
                                        "1":"SELECT * FROM TECNIQUE;",
                                        "2":"SELECT * FROM TECNIQUE WHERE TECNIQUE.tecnique=\'%s\';",
                                        "3":"SELECT * FROM TECNIQUE WHERE TECNIQUE.tecnique_short_description LIKE \'%%%s%%\';"
                                       }
                                       
            #esecuzione sul database delle queries selezionate in input dall'utente per l'export dei dati dalla tabella TECNIQUE#
            for code in tecnique_query_selection.split(","):
                
                #allocazione di una variabile di tipo stringa per memorizzare il path dinamico di salvataggio del file .csv di export dalle varie tabelle#
                save_file_path="./OUTPUT/table_"+table_name+"_query_number_"+str(code)+"_export_data_results_"+ str(date.year)+"-"+str(date.month)+"-"+str(date.day)+"_"+str(int(date.hour))+"-"+str(date.minute)+"-"+str(date.second)+".csv"
                
                if(code == "1"):
                    result_header=field_dictionary["TECNIQUE"]
                    cursor.execute(tecnique_queries[code])
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "2"):
                    result_header=field_dictionary["TECNIQUE"]
                    tecnique_list=input("\nenter tecnique (i.e. QPCR or QPCR,RTPCR,...): ").split(",")
                    tecnique_query_results=[]
                    for tecnique in tecnique_list:
                        cursor.execute(tecnique_queries[code] % tecnique)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            tecnique_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=tecnique_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "3"):
                    result_header=field_dictionary["TECNIQUE"]
                    tecnique_term_list=input("\nenter term to search into field tecnique_short_description (i.e. Electrophoresis or Electrophoresis,Spectrometry,Chromatography,...): ").split(",")
                    tecnique_term_query_results=[]
                    for tecnique_term in tecnique_term_list:
                        cursor.execute(tecnique_queries[code] % tecnique_term)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            tecnique_term_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=tecnique_term_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                        
        #menu di selezione come parametro di input delle queries specifiche per la tabella TAG#
        if(table_name == "TAG"):
            print(
                    "\nqueires selection menu to export data from table TAG:\n",
                    "\n1: to extract all table records;",
                    "\n2: to extract all record fields relative to an input keyword_tag;",
                    "\n3: to extract all record fields relative to an input term to search into field keyword_tags;",
                    "\n4: to extract all record fields relative to an input term to search into field tags_short_description;"
                    ) 

            #variabili richieste come parametri di input all'utente: queries selezionate per l'export dalla tabella TAG del database MIQUALAT#
            tag_query_selection=input("\nenter TAG table queries selection numbers (i.e. 4 or 1,2,3): ")
            
            #dizionario delle queries specifiche per la tabella TAG#
            tag_queries={
                                "1":"SELECT * FROM TAG;",
                                "2":"SELECT * FROM TAG WHERE TAG.keyword_tags=\'%s\';",
                                "3":"SELECT * FROM TAG WHERE TAG.keyword_tags LIKE \'%%%s%%\';",
                                "4":"SELECT * FROM TAG WHERE TAG.tags_short_description LIKE \'%%%s%%\';"
                               }
                                       
            #esecuzione sul database delle queries selezionate in input dall'utente per l'export dei dati dalla tabella TAG#
            for code in tag_query_selection.split(","): 

                #allocazione di una variabile di tipo stringa per memorizzare il path dinamico di salvataggio del file .csv di export dalle varie tabelle#
                save_file_path="./OUTPUT/table_"+table_name+"_query_number_"+str(code)+"_export_data_results_"+ str(date.year)+"-"+str(date.month)+"-"+str(date.day)+"_"+str(int(date.hour))+"-"+str(date.minute)+"-"+str(date.second)+".csv"

                if(code == "1"):
                    result_header=field_dictionary["TAG"]
                    cursor.execute(tag_queries[code])
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "2"):
                    result_header=field_dictionary["TAG"]
                    keyword_tags_list=input("\nenter keyword_tags (i.e. glutathione or glutathione,mammary gland,peak lactation,...): ").split(",")
                    keyword_tags_query_results=[]
                    for keyword_tag in keyword_tags_list:
                        cursor.execute(tag_queries[code] % keyword_tag)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            keyword_tags_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=keyword_tags_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "3"):
                    result_header=field_dictionary["TAG"]
                    tag_term_list=input("\nenter term to search into field keyword_tags (i.e. GWAS or GWAS,Holstein,lactation,...): ").split(",")
                    tag_term_query_results=[]
                    for tag_term in tag_term_list:
                        cursor.execute(tag_queries[code] % tag_term)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            tag_term_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=tag_term_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "4"):
                    result_header=field_dictionary["TAG"]
                    tag_term_list=input("\nenter term to search into field tags_short_description (i.e. breed or bredd,different stage of lactation,mammary,...): ").split(",")
                    tag_term_query_results=[]
                    for tag_term in tag_term_list:
                        cursor.execute(tag_queries[code] % tag_term)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            tag_term_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=tag_term_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")        
                        
        #menu di selezione come parametro di input delle queries specifiche per la tabella PUBLICATION#
        if(table_name == "PUBLICATION"):
            print(
                    "\nqueires selection menu to export data from table PUBLICATION:\n",
                    "\n1: to extract all table records;",
                    "\n2: to extract all record fields of a paper relative to an input pubmed_ID;",
                    "\n3: to extract all record fields of a paper relative to an input doi;",
                    "\n4: to extract all record fields of all papers relative to an input journal;"
                    "\n5: to extract all record fields of all papers relative to an input author to search into field authors_name;"
                    "\n6: to extract all record fields of all papers relative to an input publication year date;"
                    ) 

            #variabili richieste come parametri di input all'utente: queries selezionate per l'export dalla tabella PUBLICATION del database MIQUALAT#
            publication_query_selection=input("\nenter PUBLICATION table queries selection numbers (i.e. 4 or 1,2,3): ")
            
            #dizionario delle queries specifiche per la tabella PUBLICATION#
            publication_queries={
                                            "1":"SELECT * FROM PUBLICATION;",
                                            "2":"SELECT * FROM PUBLICATION WHERE PUBLICATION.pubmed_ID=%s;",
                                            "3":"SELECT * FROM PUBLICATION WHERE PUBLICATION.doi=\'%s\';",
                                            "4":"SELECT * FROM PUBLICATION WHERE PUBLICATION.article_journal=\'%s\';",
                                            "5":"SELECT * FROM PUBLICATION WHERE PUBLICATION.article_authors LIKE \'%%%s%%\';",
                                            "6":"SELECT * FROM PUBLICATION WHERE PUBLICATION.publication_year=%s;"
                                          }
                                          
            #esecuzione sul database delle queries selezionate in input dall'utente per l'export dei dati dalla tabella TAG#
            for code in publication_query_selection.split(","): 

                #allocazione di una variabile di tipo stringa per memorizzare il path dinamico di salvataggio del file .csv di export dalle varie tabelle#
                save_file_path="./OUTPUT/table_"+table_name+"_query_number_"+str(code)+"_export_data_results_"+ str(date.year)+"-"+str(date.month)+"-"+str(date.day)+"_"+str(int(date.hour))+"-"+str(date.minute)+"-"+str(date.second)+".csv"         

                if(code == "1"):
                    result_header=field_dictionary["PUBLICATION"]
                    cursor.execute(publication_queries[code])
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "2"):
                    result_header=field_dictionary["PUBLICATION"]
                    pubmed_ID_list=input("\nenter pubmed_ID (i.e. 29024632 or 29024632,29024999,...): ").split(",")
                    pubmed_ID_query_results=[]
                    for pubmed_ID in pubmed_ID_list:
                        cursor.execute(publication_queries[code] % pubmed_ID)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            pubmed_ID_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=pubmed_ID_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "3"):
                    result_header=field_dictionary["PUBLICATION"]
                    doi_list=input("\nenter doi (i.e. 10.1016/j.bbrc.2017.10.038 or 10.1016/j.bbrc.2017.10.038,10.1016/j.bbrc.2017.10.999,...): ").split(",")
                    doi_query_results=[]
                    for doi in doi_list:
                        cursor.execute(publication_queries[code] % doi)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            doi_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=doi_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "4"):
                    result_header=field_dictionary["PUBLICATION"]
                    journal_list=input("\nenter scientific journal name (i.e. DNAResearch or DNAResearch,Nature,Bioinformatics,...): ").split(",")
                    journal_query_results=[]
                    for journal in journal_list:
                        cursor.execute(publication_queries[code] % journal)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            journal_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=journal_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "5"):
                    result_header=field_dictionary["PUBLICATION"]
                    author_list=input("\nenter author name to search into field article_authors (i.e. Francis Crick or Francis Crick,James Watson,Crick F.,Watson J.,...): ").split(",")
                    author_query_results=[]
                    for author in author_list:
                        cursor.execute(publication_queries[code] % author)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            author_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=author_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "6"):
                    result_header=field_dictionary["PUBLICATION"]
                    year_list=input("\nenter publication year date (i.e. 2020 or 2020,2019,2018,...): ").split(",")
                    year_query_results=[]
                    for year in year_list:
                        cursor.execute(publication_queries[code] % year)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            year_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=year_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")

        #menu di selezione come parametro di input delle queries specifiche per la tabella VARIANT#
        if(table_name == "VARIANT"):
            print(
                    "\nqueires selection menu to export data from table VARIANT:\n",
                    "\n1: to extract all table records;",
                    "\n2: to extract all record fields relative to an input variant_name;"
                    "\n3: to extract all record fields of all variants relative to an input ensembl_gene_ID;"
                    "\n4: to extract all record fields of all variant relative to an input gene_name of an input species;"
                    "\n5: to extract all record fields of all variants and the respective ensembl_gene_ID and gene_name relative to an input species;",
                    "\n6: to extract all record fields of all variants and the respective ensembl_gene_ID and gene_name relative to an input species and an input chromosome;"
                    ) 

            #variabili richieste come parametri di input all'utente: queries selezionate per l'export dalla tabella VARIANT del database MIQUALAT#
            variant_query_selection=input("\nenter VARIANT table queries selection numbers (i.e. 4 or 1,2,3): ")        
                
            #dizionario delle queries specifiche per la tabella VARIANT#
            variant_queries={
                                     "1":"SELECT * FROM VARIANT;",
                                     "2":"SELECT * FROM VARIANT WHERE VARIANT.variant_name=\'%s\';",
                                     "3":"SELECT DISTINCT PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID,VARIANT.* FROM PUB_GEN_VAR_TEC_TAG,VARIANT WHERE PUB_GEN_VAR_TEC_TAG.variant_name=VARIANT.variant_name AND PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID=\'%s\';",
                                     "4":"SELECT DISTINCT GENE.gene_name,VARIANT.* FROM GENE,PUB_GEN_VAR_TEC_TAG,VARIANT WHERE GENE.ensembl_gene_ID=PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID AND PUB_GEN_VAR_TEC_TAG.variant_name=VARIANT.variant_name AND GENE.gene_name=\'%s\' AND VARIANT.species=\'%s\' AND GENE.species=VARIANT.species;",
                                     "5":"SELECT DISTINCT VARIANT.*,PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID,GENE.gene_name FROM GENE,PUB_GEN_VAR_TEC_TAG,VARIANT WHERE GENE.ensembl_gene_ID=PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID AND PUB_GEN_VAR_TEC_TAG.variant_name=VARIANT.variant_name AND VARIANT.species=\'%s\' AND GENE.species=VARIANT.species;",
                                     "6":"SELECT DISTINCT VARIANT.*,PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID,GENE.gene_name FROM GENE,PUB_GEN_VAR_TEC_TAG,VARIANT WHERE GENE.ensembl_gene_ID=PUB_GEN_VAR_TEC_TAG.ensembl_gene_ID AND PUB_GEN_VAR_TEC_TAG.variant_name=VARIANT.variant_name AND VARIANT.species=\'%s\' AND VARIANT.chromosome=%s AND GENE.species=VARIANT.species;"
                                     }

            #esecuzione sul database delle queries selezionate in input dall'utente per l'export dei dati dalla tabella VARIANT#
            for code in variant_query_selection.split(","): 

                #allocazione di una variabile di tipo stringa per memorizzare il path dinamico di salvataggio del file .csv di export dalle varie tabelle#
                save_file_path="./OUTPUT/table_"+table_name+"_query_number_"+str(code)+"_export_data_results_"+ str(date.year)+"-"+str(date.month)+"-"+str(date.day)+"_"+str(int(date.hour))+"-"+str(date.minute)+"-"+str(date.second)+".csv"         

                if(code == "1"):
                    result_header=field_dictionary["VARIANT"]
                    cursor.execute(variant_queries[code])
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "2"):
                    result_header=["variant_name","variant_type","chromosome","position","reference_allele","alternative_allele","rs_ID","species","refseq"]
                    variant_name_list=input("\nenter variant_name (i.e. bosTau11_29:123456789_A|G or bosTau11_29:123456789_A|G,hg38_1:146793_A|G,...): ").split(",")
                    variant_name_query_results=[]
                    for variant_name in variant_name_list:
                        cursor.execute(variant_queries[code] % variant_name)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            variant_name_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=variant_name_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "3"):
                    result_header=["ensembl_gene_ID","variant_name","variant_type","chromosome","position","reference_allele","alternative_allele","rs_ID","species","refseq"]
                    ensembl_gene_ID_list=input("\nenter ensembl_gene_ID (i.e. ENSBTAG00000000009 or ENSBTAG00000000010,ENSBTAG00000000011,ENSBTAG00000000012,...): ").split(",")
                    IDs_query_results=[]
                    for ID in ensembl_gene_ID_list:
                        cursor.execute(variant_queries[code] % ID)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            IDs_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=IDs_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "4"):
                    result_header=["gene_name","variant_name","variant_type","chromosome","position","reference_allele","alternative_allele","rs_ID","species","refseq"]
                    cursor.execute(variant_queries[code] % (input("\nenter gene_name (i.e. UBL7 or UBL7,TDH,TTC33,...): "),input("\nenter species (i.e. Bos taurus or Homo sapiens): ")))
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "5"):
                    result_header=["variant_name","variant_type","chromosome","position","reference_allele","alternative_allele","rs_ID","species","refseq","ensembl_gene_ID","gene_name"]
                    cursor.execute(variant_queries[code] % input("\nenter species (i.e. Bos taurus or Homo sapiens): "))
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "6"):
                    result_header=["variant_name","variant_type","chromosome","position","reference_allele","alternative_allele","rs_ID","species","refseq","ensembl_gene_ID","gene_name"]
                    cursor.execute(variant_queries[code] % (input("\nenter species (i.e. Bos taurus or Homo sapiens): "),input("\nenter chromosome (i.e. 8): ")))
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")        

        #menu di selezione come parametro di input delle queries specifiche per la tabella GEN_KEGG#
        if(table_name == "GEN_KEGG"):
            print(
                    "\nqueires selection menu to export data from table GEN_KEGG:\n",
                    "\n1: to extract all table records;",
                    "\n2: to extract kegg_id,ensembl_gene_ID,gene_name,species of all genes relative to an input compound name (or pathway or molecule) to search into field kegg_object_name;",
                    "\n3: to extract all KEGG record fields related to an input species and an input kegg_object_type (gene, pathway, protein, enzyme or others);"
                    ) 

            #variabili richieste come parametri di input all'utente: queries selezionate per l'export dalla tabella GEN_KEGG del database MIQUALAT#
            gen_kegg_query_selection=input("\nenter GEN_KEGG table queries selection numbers (i.e. 4 or 1,2,3): ")        

            #dizionario delle queries specifiche per la tabella GEN_KEGG#
            gen_kegg_queries={
                                          "1":"SELECT * FROM GEN_KEGG;",
                                          "2":"SELECT KEGG.kegg_object_name,GEN_KEGG.kegg_ID,GEN_KEGG.ensembl_gene_ID,GENE.gene_name,GENE.species FROM KEGG,GEN_KEGG,GENE WHERE KEGG.kegg_ID=GEN_KEGG.kegg_ID AND GEN_KEGG.ensembl_gene_ID=GENE.ensembl_gene_ID AND KEGG.kegg_object_name LIKE \'%%%s%%\';",
                                          "3":"SELECT KEGG.*,GENE.species FROM KEGG,GEN_KEGG,GENE WHERE KEGG.kegg_ID=GEN_KEGG.kegg_ID AND GEN_KEGG.ensembl_gene_ID=GENE.ensembl_gene_ID AND KEGG.kegg_object_type=\'%s\' AND GENE.species=\'%s\';"
                                         }

            #esecuzione sul database delle queries selezionate in input dall'utente per l'export dei dati dalla tabella GEN_KEGG#
            for code in gen_kegg_query_selection.split(","): 

                #allocazione di una variabile di tipo stringa per memorizzare il path dinamico di salvataggio del file .csv di export dalle varie tabelle#
                save_file_path="./OUTPUT/table_"+table_name+"_query_number_"+str(code)+"_export_data_results_"+ str(date.year)+"-"+str(date.month)+"-"+str(date.day)+"_"+str(int(date.hour))+"-"+str(date.minute)+"-"+str(date.second)+".csv"         

                if(code == "1"):
                    result_header=field_dictionary["GEN_KEGG"]
                    cursor.execute(gen_kegg_queries[code])
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "2"):
                    result_header=["kegg_object_name","kegg_ID","ensembl_gene_ID","gene_name","species"]
                    kegg_obj_name_list=input("\nenter compound name to search into kegg_object_name (i.e. glutathione or glutathione,other molecules name,pathways name): ").split(",")
                    kegg_obj_name_query_results=[]
                    for kegg_obj_name in kegg_obj_name_list:
                        cursor.execute(gen_kegg_queries[code] % kegg_obj_name)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            kegg_obj_name_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=kegg_obj_name_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "3"):
                    result_header=["kegg_ID","kegg_object_type","kegg_object_name","species"]
                    cursor.execute(gen_kegg_queries[code] % (input("\nenter kegg_object_type (i.e. gene or pathway or protein or enzyme or others): "),input("\nenter species (i.e. Bos taurus or Homo sapiens): ")))
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")   
        
        #menu di selezione come parametro di input delle queries specifiche per la tabella KEGG#
        if(table_name == "KEGG"):
            print(
                    "\nqueires selection menu to export data from table KEGG:\n",
                    "\n1: to extract all table records;",
                    "\n2: to extract all record fields relative to an input kegg_ID;",
                    "\n3: to extract all record fields relative to an input compound name (or pathway or molecule) to search into field kegg_object_name;"
                    ) 

            #variabili richieste come parametri di input all'utente: queries selezionate per l'export dalla tabella KEGG del database MIQUALAT#
            kegg_query_selection=input("\nenter KEGG table queries selection numbers (i.e. 4 or 1,2,3): ")

            #dizionario delle queries specifiche per la tabella KEGG#
            kegg_queries={
                                   "1":"SELECT * FROM KEGG;",
                                   "2":"SELECT KEGG.* FROM KEGG WHERE KEGG.kegg_ID=\'%s\';",
                                   "3":"SELECT KEGG.* FROM KEGG WHERE KEGG.kegg_object_name LIKE \'%%%s%%\';"
                                  }
            
            #esecuzione sul database delle queries selezionate in input dall'utente per l'export dei dati dalla tabella GEN_KEGG#
            for code in kegg_query_selection.split(","): 

                #allocazione di una variabile di tipo stringa per memorizzare il path dinamico di salvataggio del file .csv di export dalle varie tabelle#
                save_file_path="./OUTPUT/table_"+table_name+"_query_number_"+str(code)+"_export_data_results_"+ str(date.year)+"-"+str(date.month)+"-"+str(date.day)+"_"+str(int(date.hour))+"-"+str(date.minute)+"-"+str(date.second)+".csv"         

                if(code == "1"):
                    result_header=field_dictionary["KEGG"]
                    cursor.execute(kegg_queries[code])
                    query_results=[list(query_result) for query_result in cursor]
                    result_df=pd.DataFrame.from_records(data=query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "2"):
                    result_header=field_dictionary["KEGG"]
                    kegg_ID_list=input("\nenter kegg_ID (kegg code of gene, pathway, protein, enzyme...etc.)(i.e. bta:281495 or bta:281495,bta:281210,bta:615507,...): ").split(",")
                    kegg_ID_query_results=[]
                    for kegg_ID in kegg_ID_list:
                        cursor.execute(kegg_queries[code] % kegg_ID)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            kegg_ID_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=kegg_ID_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")
                elif(code == "3"):
                    result_header=field_dictionary["KEGG"]
                    kegg_obj_name_list=input("\nenter compound name to search into kegg_object_name (i.e. glutathione or glutathione,other molecules name,pathways name): ").split(",")
                    kegg_obj_name_query_results=[]
                    for kegg_obj_name in kegg_obj_name_list:
                        cursor.execute(kegg_queries[code] % kegg_obj_name)
                        query_results=[list(query_result) for query_result in cursor]
                        for result in query_results:
                            kegg_obj_name_query_results.append(result)
                    result_df=pd.DataFrame.from_records(data=kegg_obj_name_query_results,columns=result_header)
                    display(result_df)
                    save_file_selection=input(save_file_string)
                    if(save_file_selection == "yes"):
                        result_df.to_csv(path_or_buf=save_file_path,sep=",",header=True,index=False,na_rep="NULL")