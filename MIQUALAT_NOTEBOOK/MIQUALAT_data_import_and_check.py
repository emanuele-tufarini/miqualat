#importazione dei moduli csv per la lettura dei file da inserire nel database e del modulo MySQLdb per connettersi al DATABASE MIQUALAT e della libreria getpass dalla quale viene usato il modulo getpass per mascherare la password di accesso al database server#
import csv
import MySQLdb
import getpass

#funzione che effettua il controllo dei campi delle tabelle di natura numerica intera#
def string_to_integer_checker(string):
    try:
        int(string)
        return(True)
    except:
        return(False)

#funzione che effettua l'importazione dei dati nel database MIQUALAT dai file CSV dell'utente#
def database_importer(host,user,pswd,db,csv_file_path,table_name,field_dictionary):
    mydb=MySQLdb.connect(host=host, user=user, passwd=pswd, db=db)
    cursor=mydb.cursor()
    csv_data=csv.reader(open(csv_file_path))
    header=",".join(next(csv_data))
    for entry in csv_data:
        entry=[None if field=="NULL" else field for field in entry]
        cursor.execute("INSERT INTO "+table_name+"("+field_dictionary[table_name][0]+") VALUES"+field_dictionary[table_name][1],entry)
    mydb.commit()
    cursor.close()
    print ("\n"+table_name+" has been successully imported into the database")
    
#funzione che effettua il check delle entries presenti nel CSV file dell'utente rispetto ad i record presenti nel database MIQUALAT#
def database_security_checker(host,user,pswd,db,csv_file_path,table_name):
    
    #variabili locali#
    warning_flag=0
    global_warning="\n\n#### WARNING[global]: your table: "+table_name+" has not been uploaded on database: "+db+" please check the file: "+csv_file_path+" for precedent existing WARNINGS ####\n"
    field_dictionary={
    "GENE":["ensembl_gene_ID,gene_name,gene_short_description,refseq,species,chromosome,start_coordinate,end_coordinate,strand","(%s, %s,%s, %s, %s, %s,%s, %s, %s)",["string","string","string","string","string","int","int","int","int"]],
    "PUB_GEN_VAR_TEC_TAG":["integer_progressive_ID,pubmed_ID,ensembl_gene_ID,variant_name,tecnique,keyword_tags,relationship_note","(%s, %s, %s, %s,%s, %s, %s)",["null","int","string","string","string","string","string"]],
    "GEN_KEGG":["ensembl_gene_ID,kegg_ID","(%s, %s)",["string","string"]],
    "KEGG":["kegg_ID,kegg_object_type,kegg_object_name","(%s, %s, %s)",["string","string","string"]],
    "PUBLICATION":["pubmed_ID,doi,article_title,article_authors,article_journal,publication_year","(%s, %s, %s, %s, %s, %s)",["int","string","string","string","string","int"]],
    "TAG":["keyword_tags,tags_short_description","(%s, %s)",["string","string"]],
    "TECNIQUE":["tecnique,tecnique_short_description","(%s, %s)",["string","string"]],
    "VARIANT":["variant_name,variant_type,chromosome,position,reference_allele,alternative_allele,rs_ID,species,refseq","(%s, %s, %s, %s,%s,%s,%s,%s,%s)",["string","string","int","int","string","string","string","string","string"]]
    }
    entries_list=[]
    PUB_GEN_VAR_TEC_TAG_entries_list=[]
    
    #CONNESSIONE AL SERVER DOVE È ALLOCATO IL DATABASE#
    mydb=MySQLdb.connect(host=host, user=user, passwd=pswd, db=db)
    
    #esecuzione della query generica sul database per estrarre tutti i record presenti in una determinata tabella data come parametro di input#
    cursor=mydb.cursor()
    cursor.execute("SELECT * FROM "+table_name)
    query_results=[list(query_result) for query_result in cursor]
    
    #adattamento sintassi python-mysql/conversione dei fields NONE in NULL e conversione dei fields tutti in formato stringa e in carattere minuscolo#
    for i,record in enumerate(query_results):
        query_results[i]=["NULL" if field==None else str(field) for field in record]
    
    #CONTROLLO DEI FILE DI INPUT IN FORMATO .csv#
   
    #opening csv data file#
    csv_data=csv.reader(open(csv_file_path))
    
    #checking for header integrity#
    header=",".join(next(csv_data))
    if(header != field_dictionary[table_name][0]):
        warning_flag=1
        return(print("WARNING["+str(warning_flag)+"] : header of csv file: "+csv_file_path+" is different from table header: "+table_name,global_warning))
    
    #reading csv data entries#
    for i,entry in enumerate(csv_data):
        
        #check for csv data file entries fields number#
        if(len(entry) != len(field_dictionary[table_name][0].split(","))):
            warning_flag=2
            return(print("WARNING["+str(warning_flag)+"]: entry at line number: "+str(i+2)+" of csv file: "+csv_file_path+" has a wrong number of fields respect the table: "+table_name,global_warning))
        
        #check for entry duplicates#
        if(",".join(entry).lower() not in entries_list):
            entries_list.append(",".join(entry).lower())
        else:
            warning_flag=3
            return(print("WARNING["+str(warning_flag)+"]: in csv data file: "+csv_file_path+" the entry: "+str(entry)+" is duplicated at least one time",global_warning))

        #controllo degli entry fields di natura numerica intera#
        for p,field in enumerate(entry):
            if(field_dictionary[table_name][2][p] == "int" and string_to_integer_checker(field) == False):
                warning_flag=4
                return(print("WARNING["+str(warning_flag)+"]: in csv data file: "+csv_file_path+" the entry: "+str(entry)+" at line: "+str(i+2)+" contains the field: "+field_dictionary[table_name][0].split(",")[p]+"="+field+" that must be setted up with integer value and not alphanumerical value",global_warning))
        
        #CONTROLLO DELL'ESISTENZA DELLE FOREIGN_KEYS PER LE TABELLE RELAZIONALI DEL DATABASE MIQUALAT#
        
        #controllo dell'esistenza delle foreign keys della tabella PUB_GEN_VAR_TEC_TAG nelle rispettive tabelle del database MIQUALAT#
        if(table_name == "PUB_GEN_VAR_TEC_TAG"):
            pubmed_ID=entry[1]
            if(pubmed_ID != "NULL"):
                cursor.execute("SELECT PUBLICATION.pubmed_ID FROM PUBLICATION WHERE PUBLICATION.pubmed_ID="+pubmed_ID)
                pubmed_ID_query_result=[query_result for query_result in cursor]
                if(pubmed_ID_query_result == []):
                    warning_flag=5
                    return(print("WARNING["+str(warning_flag)+"]: for the table PUB_GEN_VAR_TEC_TAG, the foreign_key pubmed_ID: "+pubmed_ID+" is not present in table PUBLICATION, please upload require data in PUBLICATION",global_warning))
            else:
                warning_flag=6
                return(print("WARNING["+str(warning_flag)+"]: the field PUB_GEN_VAR_TEC_TAG.pubmed_ID can't be setted up with NULL value at entry number: "+str(i+2),global_warning))
            ensembl_gene_ID=entry[2]
            if(ensembl_gene_ID != "NULL"):
                cursor.execute("SELECT GENE.ensembl_gene_ID FROM GENE WHERE GENE.ensembl_gene_ID=\'"+ensembl_gene_ID+"\'")
                ensembl_gene_ID_query_result=[query_result for query_result in cursor]
                if(ensembl_gene_ID_query_result == []):
                    warning_flag=7
                    return(print("WARNING["+str(warning_flag)+"]: for the table PUB_GEN_VAR_TEC_TAG, the foreign_key ensembl_gene_ID: "+ensembl_gene_ID+" is not present in table GENE, please verify the correct ensembl_gene_ID",global_warning))
            variant_name=entry[3]
            if(variant_name != "NULL"):
                cursor.execute("SELECT VARIANT.variant_name FROM VARIANT WHERE VARIANT.variant_name=\'"+variant_name+"\'")
                variant_name_query_result=[query_result for query_result in cursor]
                if(variant_name_query_result == []):
                    warning_flag=8
                    return(print("WARNING["+str(warning_flag)+"]: for the table PUB_GEN_VAR_TEC_TAG, the foreign_key variant_name: "+variant_name+" is not present in table VARIANT, please upload require data in VARIANT",global_warning))
            tecnique=entry[4]
            if(tecnique != "NULL"):
                cursor.execute("SELECT TECNIQUE.tecnique FROM TECNIQUE WHERE TECNIQUE.tecnique=\'"+tecnique+"\'")
                tecnique_query_result=[query_result for query_result in cursor]
                if(tecnique_query_result == []):
                    warning_flag=9
                    return(print("WARNING["+str(warning_flag)+"]: for the table PUB_GEN_VAR_TEC_TAG, the foreign_key tecnique: "+tecnique+" is not present in table TECNIQUE, please upload require data in TECNIQUE",global_warning))
            keyword_tags=entry[5]
            if(keyword_tags != "NULL"):
                cursor.execute("SELECT TAG.keyword_tags FROM TAG WHERE TAG.keyword_tags=\'"+keyword_tags+"\'")
                keyword_tags_query_result=[query_result for query_result in cursor]
                if(keyword_tags_query_result == []):
                    warning_flag=10
                    return(print("WARNING["+str(warning_flag)+"]: for the table PUB_GEN_VAR_TEC_TAG, the foreign_key keyword_tags: "+keyword_tags+" is not present in table TAG, please upload require data in TAG",global_warning))
    
            #controllo speciale per la tabella PUB_GEN_VAR_TEC_TAG per monitorare la presenza di entries duplicate in relazione ai campi delle foreign_keys della tabella nel file .csv#
            if(",".join(entry[1:-1]).lower() not in PUB_GEN_VAR_TEC_TAG_entries_list):
                PUB_GEN_VAR_TEC_TAG_entries_list.append(",".join(entry[1:-1]).lower())
            else:
                warning_flag=11
                return(print("WARNING["+str(warning_flag)+"]: in csv data file: "+csv_file_path+" the entry: "+str(entry)+" is duplicated, in the foreign_keys core entry with the exclusion of relationship_note field, at least one time",global_warning))
        
            #confronto speciale tra le entries del file csv data di importazione della tabella PUB_GEN_VAR_TEC_TAG ed i records risultato della query sulla tabella PUB_GEN_VAR_TEC_TAG del database#
            for record in query_results:
                if(",".join(entry[1:-1]).lower() == ",".join(record[1:-1]).lower()):
                    warning_flag=12
                    return(print("WARNING["+str(warning_flag)+"]: entry: "+str(entry)+", at line number: "+str(i+2)+",is already in database: "+db+" in table: "+table_name+" at least the foreign_keys entry core",global_warning))
        
        #controllo dell'esistenza delle foreign keys della tabella GEN_KEGG nelle rispettive tabelle del database MIQUALAT#
        elif(table_name == "GEN_KEGG"):
            ensembl_gene_ID=entry[0]
            if(ensembl_gene_ID != "NULL"):
                cursor.execute("SELECT GENE.ensembl_gene_ID FROM GENE WHERE GENE.ensembl_gene_ID=\'"+ensembl_gene_ID+"\'")
                ensembl_gene_ID_query_result=[query_result for query_result in cursor]
                if(ensembl_gene_ID_query_result == []):
                    warning_flag=13
                    return(print("WARNING["+str(warning_flag)+"]: for the table GEN_KEGG, the foreign_key ensembl_gene_ID: "+ensembl_gene_ID+" is not present in table GENE, please upload require data in GENE",global_warning))
            else:
                warning_flag=14
                return(print("WARNING["+str(warning_flag)+"]: the field GEN_KEGG.ensembl_gene_ID can't be setted up with NULL value at entry number: "+str(i+2),global_warning))
            kegg_ID=entry[1]
            if(kegg_ID != "NULL"):
                cursor.execute("SELECT KEGG.kegg_ID FROM KEGG WHERE KEGG.kegg_ID=\'"+kegg_ID+"\'")
                kegg_ID_query_result=[query_result for query_result in cursor]
                if(kegg_ID_query_result == []):
                    warning_flag=15
                    return(print("WARNING["+str(warning_flag)+"]: for the table GEN_KEGG, the foreign_key kegg_ID: "+kegg_ID+" is not present in table KEGG, please upload require data in KEGG",global_warning))
            else:
                warning_flag=16
                return(print("WARNING["+str(warning_flag)+"]: the field GEN_KEGG.kegg_ID can't be setted up with NULL value at entry number: "+str(i+2),global_warning))
            
            #controllo relativo alle primary_keys della tabella relazionale GEN_KEGG, verifica che non siano già inserite nella tabella del database#
            if(ensembl_gene_ID != "NULL" and kegg_ID != "NULL"):
                cursor.execute("SELECT * FROM GEN_KEGG WHERE GEN_KEGG.ensembl_gene_ID=\'"+ensembl_gene_ID+"\' AND GEN_KEGG.kegg_ID=\'"+kegg_ID+"\'")
                ensembl_gene_ID_and_kegg_ID_query_result=[query_result for query_result in cursor]
                if(ensembl_gene_ID_and_kegg_ID_query_result != []):
                    warning_flag=17
                    return(print("WARNING["+str(warning_flag)+"]: for the table GEN_KEGG, the primary_key (ensembl_gene_ID,kegg_ID): ("+ensembl_gene_ID+","+kegg_ID+") is already present in table GEN_KEGG, please control records data in GEN_KEGG on database MIQUALAT",global_warning))
        
        #CONTROLLO RELATIVO ALLE PRIMARY_KEYS, VERIFICA CHE NON SIANO GIÀ INSERITE NELLE TABELLE DEL DATABASE, ad eccezione di PUB_GEN_VAR_TEC_TAG e di GEN_KEGG#
        elif(table_name == "PUBLICATION"):
            pubmed_ID=entry[0]
            if(pubmed_ID != "NULL"):
                cursor.execute("SELECT PUBLICATION.pubmed_ID FROM PUBLICATION WHERE PUBLICATION.pubmed_ID="+pubmed_ID)
                pubmed_ID_query_result=[query_result for query_result in cursor]
                if(pubmed_ID_query_result != []):
                    warning_flag=18
                    return(print("WARNING["+str(warning_flag)+"]: for the table PUBLICATION, the primary_key pubmed_ID: "+pubmed_ID+" is already present in table PUBLICATION, please control records data in PUBLICATION on database MIQUALAT",global_warning))
            else:
                warning_flag=19
                return(print("WARNING["+str(warning_flag)+"]: the field PUBLICATION.pubmed_ID can't be setted up with NULL value at entry number: "+str(i+2),global_warning))
        elif(table_name == "GENE"):
            ensembl_gene_ID=entry[0]
            if(ensembl_gene_ID != "NULL"):
                cursor.execute("SELECT GENE.ensembl_gene_ID FROM GENE WHERE GENE.ensembl_gene_ID=\'"+ensembl_gene_ID+"\'")
                ensembl_gene_ID_query_result=[query_result for query_result in cursor]
                if(ensembl_gene_ID_query_result != []):
                    warning_flag=20
                    return(print("WARNING["+str(warning_flag)+"]: for the table GENE, the primary_key ensembl_gene_ID: "+ensembl_gene_ID+" is already present in table GENE, please control records data in GENE on database MIQUALAT",global_warning))
            else:
                warning_flag=21
                return(print("WARNING["+str(warning_flag)+"]: the field GENE.ensembl_gene_ID can't be setted up with NULL value at entry number: "+str(i+2),global_warning))
        elif(table_name == "TECNIQUE"):
            tecnique=entry[0]
            if(tecnique != "NULL"):
                cursor.execute("SELECT TECNIQUE.tecnique FROM TECNIQUE WHERE TECNIQUE.tecnique=\'"+tecnique+"\'")
                tecnique_query_result=[query_result for query_result in cursor]
                if(tecnique_query_result != []):
                    warning_flag=22
                    return(print("WARNING["+str(warning_flag)+"]: for the table TECNIQUE, the primary_key tecnique: "+tecnique+" is already present in table TECNIQUE, please control records data in TECNIQUE on database MIQUALAT",global_warning))
            else:
                warning_flag=23
                return(print("WARNING["+str(warning_flag)+"]: the field TECNIQUE.tecnique can't be setted up with NULL value at entry number: "+str(i+2),global_warning))
        elif(table_name == "VARIANT"):
            variant_name=entry[0]
            if(variant_name != "NULL"):
                cursor.execute("SELECT VARIANT.variant_name FROM VARIANT WHERE VARIANT.variant_name=\'"+variant_name+"\'")
                variant_name_query_result=[query_result for query_result in cursor]
                if(variant_name_query_result != []):
                    warning_flag=24
                    return(print("WARNING["+str(warning_flag)+"]: for the table VARIANT, the primary_key variant_name: "+variant_name+" is already present in table VARIANT, please control records data in VARIANT on database MIQUALAT",global_warning))
            else:
                warning_flag=25
                return(print("WARNING["+str(warning_flag)+"]: the field VARIANT.variant_name can't be setted up with NULL value at entry number: "+str(i+2),global_warning))
        elif(table_name == "TAG"):
            keyword_tags=entry[0]
            if(keyword_tags != "NULL"):
                cursor.execute("SELECT TAG.keyword_tags FROM TAG WHERE TAG.keyword_tags=\'"+keyword_tags+"\'")
                keyword_tags_query_result=[query_result for query_result in cursor]
                if(keyword_tags_query_result != []):
                    warning_flag=26
                    return(print("WARNING["+str(warning_flag)+"]: for the table TAG, the primary_key keyword_tags: "+keyword_tags+" is already present in table TAG, please control records data in TAG on database MIQUALAT",global_warning))
            else:
                warning_flag=27
                return(print("WARNING["+str(warning_flag)+"]: the field TAG.keyword_tags can't be setted up with NULL value at entry number: "+str(i+2),global_warning))
        elif(table_name == "KEGG"):
            kegg_ID=entry[0]
            if(kegg_ID != "NULL"):
                cursor.execute("SELECT KEGG.kegg_ID FROM KEGG WHERE KEGG.kegg_ID=\'"+kegg_ID+"\'")
                kegg_ID_query_result=[query_result for query_result in cursor]
                if(kegg_ID_query_result != []):
                    warning_flag=28
                    return(print("WARNING["+str(warning_flag)+"]: for the table KEGG, the primary_key kegg_ID: "+kegg_ID+" is already present in table KEGG, please control records data in KEGG on database MIQUALAT",global_warning))
            else:
                warning_flag=29
                return(print("WARNING["+str(warning_flag)+"]: the field KEGG.kegg_ID can't be setted up with NULL value at entry number: "+str(i+2),global_warning))
        
        #confronto tra le entries del file csv data di importazione ed i records risultato della query sul database [in questa casistica il codice non dovrebbe entrarci quasi mai ma viene lasciata come ultimo controllo se tutti gli altri fallissero]#
        for record in query_results:
            if(",".join(entry).lower() == ",".join(record).lower()):
                warning_flag=30
                return(print("WARNING["+str(warning_flag)+"]: entry: "+str(entry)+", at line number: "+str(i+2)+",is already in database: "+db+" in table: "+table_name,global_warning))
    
    #controllo dello stato della variabile flag/ se flag == 0 allora non ci sono errori ed avviene l'importazione del csv file sulla tabella del database MIQUALAT#
    if(warning_flag == 0):
        database_importer(host,user,pswd,db,csv_file_path,table_name,field_dictionary)

#funziona che permette di effettuare la selezione delle tabelle e dei dati da importare#
def database_import_data_selector(file_path):
    
    #definizione di una variabile locale di tipo dizionario per la selezione dell'input da importare nel database#
    table_dict={
    "0":["GENE","KEGG","GEN_KEGG","PUBLICATION","TECNIQUE","TAG","VARIANT","PUB_GEN_VAR_TEC_TAG"],
    "1":"GENE",
    "2":"KEGG",
    "3":"GEN_KEGG",
    "4":"PUBLICATION",
    "5":"TECNIQUE",
    "6":"TAG",
    "7":"VARIANT",
    "8":"PUB_GEN_VAR_TEC_TAG"
    }
    
    #variabili richieste come parametri di input all'utente: database username e password#
    username=input("enter your username: ")
    password=getpass.getpass("enter your password: ")
    
    #print del menu a tendina di seleziona delle tabelle da importare#
    print("\nimport selection menu: ")
    for key in table_dict.keys():
        if(type(table_dict[key]) == list):
            print("enter "+key+" to upload data in database MIQUALAT following tables: "+",".join(table_dict[key])+";")
        else:
            print("enter "+key+" to upload data in database MIQUALAT following tables: "+table_dict[key]+";")

    #variabili richieste come parametri di input all'utente: tabelle selezionate per l'import nel database#
    selection=input("\nenter tables selection numbers (i.e. 0 or 5 or 1,2,3): ")
    
    #chiamata della funzione database_security_checker con i risultati di selezione ed i parametri impostati dall'utente#
    if(len(selection) == 0):
        print("WARNING: please enter a selection code in range 0-8")
    elif(len(selection) == 1):
        if(selection in table_dict.keys()):
            if(selection == "0"):
                for table_name in table_dict[selection]:
                    csv_file_name=input("\nfor table: "+table_name+" enter csv file name: ")
                    database_security_checker("localhost",username,password,"MIQUALAT",file_path+csv_file_name,table_name)
            else:
                csv_file_name=input("\nfor table: "+table_dict[selection]+" enter csv file name: ")
                database_security_checker("localhost",username,password,"MIQUALAT",file_path+csv_file_name,table_dict[selection])
        else:
            print("WARNING: the inserted code: "+selection+" is not present in the tables selection menu")
    else:
        for code in selection.split(","):
            if(code in table_dict.keys()):
                if(code == "0"):
                    for table_name in table_dict[code]:
                        csv_file_name=input("\nfor table: "+table_name+" enter csv file name: ")
                        database_security_checker("localhost",username,password,"MIQUALAT",file_path+csv_file_name,table_name)
                else:
                    csv_file_name=input("\nfor table: "+table_dict[code]+" enter csv file name: ")
                    database_security_checker("localhost",username,password,"MIQUALAT",file_path+csv_file_name,table_dict[code])
            else:
                print("WARNING: the inserted code: "+code+" is not present in the tables selection menu")