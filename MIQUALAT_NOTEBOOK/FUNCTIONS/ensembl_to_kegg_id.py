'''
emanuele.tufarini@live.com
last modification 11-2020
'''

# import modules
import os
import mygene
from Bio.KEGG import REST
    
def ensembl_to_kegg_id(ENSEMBL_GENEID,n,KEGG_NCBI,NCBI_ID_LIST,KEGG_ID_LIST,GENE_PATH,GENE_KEGG_ID,PATH_KEGG_ID):
    
    ENS_GENE_ID=open("ENS_GENE_ID.csv","a")
    ENS_PATH_ID=open("ENS_PATH_ID.csv","a")    
    
    try:
        
        mg = mygene.MyGeneInfo()
        MYRESULT = mg.getgene(ENSEMBL_GENEID)
        _ID = (str(MYRESULT.get('_id')))

        if _ID != ENSEMBL_GENEID: NCBI_ID = _ID
        elif _ID == ENSEMBL_GENEID: NCBI_ID = "NULL"
        else: NCBI_ID = "NULL"
        
        print("ENSEMBL_ID | ",ENSEMBL_GENEID," |NCBI_ID | ",NCBI_ID)
        
        if NCBI_ID == _ID:
            for e in NCBI_ID_LIST:
                if NCBI_ID == e[12:]: 
                    ind = (NCBI_ID_LIST.index(e))
                    GENE_KEGG_ID_CONV = (KEGG_ID_LIST[ind])
                    ENS_GENE_ID_WRITE=('"' + str(ENSEMBL_GENEID)+ '","' +str(GENE_KEGG_ID_CONV)+'"\n')
                    ENS_GENE_ID.write(ENS_GENE_ID_WRITE)
                    print("ENSEMBL_ID | ",ENSEMBL_GENEID," | KEGG_ID | ",GENE_KEGG_ID_CONV)

            ind_path = [i for i, x in enumerate(GENE_KEGG_ID) if x == GENE_KEGG_ID_CONV]
                        
            if type(ind_path) == int:
                KEGG_PATH_ID=(PATH_KEGG_ID[ind_path])
                ENS_PATH_ID=open("ENS_PATH_ID.csv","a")
                
                ENS_PATH_ID.write('"'+str(ENSEMBL_GENEID)+'","'+str(KEGG_PATH_ID)+'"\n')  
                
                print("ENSEMBL_ID | ",ENSEMBL_GENEID," | PATH_ID | ",KEGG_PATH_ID)
            elif type(ind_path) == list:
                for i in ind_path:
                    KEGG_PATH_ID=(PATH_KEGG_ID[i])
                    ENS_PATH_ID.write('"'+str(ENSEMBL_GENEID)+'","'+str(KEGG_PATH_ID)+'"\n')
                    print("ENSEMBL_ID | ",ENSEMBL_GENEID," | PATH_ID | ",KEGG_PATH_ID)
        print("\nall done.. gene has been converted ..\n")
    except:
        print("warning .. gene has not been found ..")

    ENS_GENE_ID.close()
    ENS_PATH_ID.close()