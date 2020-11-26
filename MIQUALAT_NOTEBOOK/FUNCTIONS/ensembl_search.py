'''
emanuele.tufarini@live.com
last modification 11-2020
'''

import ensembl_rest

def ensembl_search(species,ensembl_symbol,n):
    try:
        ENSEMBL_DICT = ensembl_rest.symbol_lookup(species,ensembl_symbol)
        with open("GENE.csv","a") as GENE:
            marker='['
            DESCRIPTION=ENSEMBL_DICT.get('description')
            if marker in DESCRIPTION:
                ind=DESCRIPTION.index(marker)
                DESCRIPTION=(DESCRIPTION[:ind])             
            print ('RESULT '+str(n)+' | SPECIES | ' + species +\
                   ' | SYMBOL | ' + ensembl_symbol +\
                   ' | ID | ' + str(ENSEMBL_DICT.get('id'))+\
                   ' | DISPLAY_NAME | ' + str(ENSEMBL_DICT.get('display_name'))+\
                   ' | DESCRIPTION | ' + str(DESCRIPTION)+\
                   ' | ASSEMBLY_NAME | ' + str(ENSEMBL_DICT.get("assembly_name"))+\
                   ' | SPECIES | ' + str(ENSEMBL_DICT.get('species'))+\
                   ' | SEQ_REGION_NAME | ' + str(ENSEMBL_DICT.get('seq_region_name'))+\
                   ' | START | ' + str(ENSEMBL_DICT.get('start'))+\
                   ' | END | ' + str(ENSEMBL_DICT.get('end'))+\
                   ' | STRAMD | ' + str(ENSEMBL_DICT.get('strand'))+'\n')
            GENE.write('"' + str(ENSEMBL_DICT.get('id'))+\
                   '","' + str(ENSEMBL_DICT.get('display_name'))+\
                   '","' + str(DESCRIPTION)+\
                   '","' + str(ENSEMBL_DICT.get("assembly_name"))+\
                   '","' + str(ENSEMBL_DICT.get('species'))+\
                   '","' + str(ENSEMBL_DICT.get('seq_region_name'))+\
                   '","' + str(ENSEMBL_DICT.get('start'))+\
                   '","' + str(ENSEMBL_DICT.get('end'))+\
                   '","' + str(ENSEMBL_DICT.get('strand'))+'"\n')
    except: print("no gene were found .. for ",species,ensembl_symbol,"\n")



