'''
emanuele.tufarini@live.com
last modification 12-2020
'''

# import modules
import os
import mygene
from Bio.KEGG import REST

#guida al funzionamento
#
#ENSEMBL_GENEID, e' l'ensembl gene_id su cui viene effettuata la query
#n, e' il numero di volte che viene eseguita la funzione
#KEGG_NCBI, e' una lista che contiene kegg_gene_id:ncbi_gene_id, da cui vengono estratti:
#>NCBI_ID_LIST
#>KEGG_ID_LIST
#GENE_PATH, e' una lista che contiene i kegg_gene_id:pathway, da cui vengono estratti:
#>GENE_KEGG_ID
#>PATH_KEGG_ID
#

#
#mygene, ensembl_gene_id > ncbi_gene_id
#kegg.REST, ncbi_gene_id > kegg_gene_id > kegg_pathway_id
#

def ensembl_to_kegg_id(ENSEMBL_GENEID,n,KEGG_NCBI,NCBI_ID_LIST,KEGG_ID_LIST,GENE_PATH,GENE_KEGG_ID,PATH_KEGG_ID):
    #apri i file in append
    ENS_GENE_ID=open("ENS_GENE_ID.csv","a")
    ENS_PATH_ID=open("ENS_PATH_ID.csv","a")    
    #catch error
    try:
        mg = mygene.MyGeneInfo()
        #crea un dizionario annidato con le informazioni sui geni
        MYRESULT = mg.getgene(ENSEMBL_GENEID)
        #l'_ID e' uguale all'elemento _ID del dizionario
        _ID = (str(MYRESULT.get('_id')))
        #se e' diverso dall'ensemble gene id esiste
        if _ID != ENSEMBL_GENEID: NCBI_ID = _ID
        #se e' uguale all'ensemble gene id non e' riportato NULL
        elif _ID == ENSEMBL_GENEID: NCBI_ID = "NULL"
        #se non rientra nelle casistiche consideralo NULL
        else: NCBI_ID = "NULL"
        #stampa l'ensembl gene id e il corrispettivo _ID (ncbi)
        print("ENSEMBL_ID | ",ENSEMBL_GENEID," |NCBI_ID | ",NCBI_ID)
        #se l'_ID (ncbi) esiste
        if NCBI_ID == _ID:
            #esegui un ciclo for per ogni elemento nella lista degli _ID (ncbi)
            for e in NCBI_ID_LIST:
                #se l'_ID (ncbi) e' uguale al codice ncbi (salta i primi 12 caratteri che non contengono il codice)
                if NCBI_ID == e[12:]: 
                    #indicizza l'elemento nella lista degli ncbi
                    ind = (NCBI_ID_LIST.index(e))
                    #associa il valore dell'kegg appena trovato (la posizione corrisponde all'ncbi)
                    GENE_KEGG_ID_CONV = (KEGG_ID_LIST[ind])
                    #scrivi nel file csv ensembl_gene,kegg_gene
                    ENS_GENE_ID_WRITE=('"' + str(ENSEMBL_GENEID)+ '","' +str(GENE_KEGG_ID_CONV)+'"\n')
                    ENS_GENE_ID.write(ENS_GENE_ID_WRITE)
                    #stampa a schermo il risultato
                    print("ENSEMBL_ID | ",ENSEMBL_GENEID," | KEGG_ID | ",GENE_KEGG_ID_CONV)
            #cerca il codice kegg nella lista (kegg,path) e indicizzala
            ind_path = [i for i, x in enumerate(GENE_KEGG_ID) if x == GENE_KEGG_ID_CONV]
            #se l'indice della path e' un intero, quindi esiste (e' riportata una sola per il gene)           
            if type(ind_path) == int:
                #scrivi il nome della path nel file
                KEGG_PATH_ID=(PATH_KEGG_ID[ind_path])
                ENS_PATH_ID=open("ENS_PATH_ID.csv","a")
                ENS_PATH_ID.write('"'+str(ENSEMBL_GENEID)+'","'+str(KEGG_PATH_ID)+'"\n')  
                print("ENSEMBL_ID | ",ENSEMBL_GENEID," | PATH_ID | ",KEGG_PATH_ID)
            #se invece e' presente una lista di indici, quindi piu' path per gene
            elif type(ind_path) == list:
                #esegui la stessa operazione per ogni indice
                for i in ind_path:
                    KEGG_PATH_ID=(PATH_KEGG_ID[i])
                    ENS_PATH_ID.write('"'+str(ENSEMBL_GENEID)+'","'+str(KEGG_PATH_ID)+'"\n')
                    print("ENSEMBL_ID | ",ENSEMBL_GENEID," | PATH_ID | ",KEGG_PATH_ID)
        #se e' andato tutto bene
        print("\nall done.. gene has been converted ..\n")
    #se qualcosa e' andato storto
    except:
        print("warning .. gene has not been found ..")
    #chiudi i file che sono stati aperti
    ENS_GENE_ID.close()
    ENS_PATH_ID.close()