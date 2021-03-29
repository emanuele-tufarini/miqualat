import requests
import sys
import pandas as pd
from IPython.display import display
import datetime

def gene_ontology_entityfinder():
    name=input("Enter your name: ")
    surname=input("Enter your surname: ")
    data = datetime.datetime.now()
    data = ("_" + str(data.year) + "-" + str(data.month) + "-" + \
            str(data.day) + "_" + str( int (data.hour)) + "-" + \
            str(data.minute) + "-" + str(data.second))
    print("[INFO] the function gene_ontology_entityfinder() retrieves gene ontology database entity code/IDs and other informations on all the GO_entity related to a gene ENSEMBL_ID or a list of gene ENSEMBL_IDs")
    ensembl_id_list=input("\nPlease enter a gene ENSEMBL_ID or a list of gene ENSEMBL_IDS comma separated [i.e. ENSBTAG00000012023 or ENSBTAG00000012023,ENSBTAG00000014486,...,ENSBTAG00000016484]:").split(',')
    server="https://rest.ensembl.org"
    output_dict={}
    for i,ensembl_id in enumerate(ensembl_id_list):
        ext="/xrefs/id/"+ensembl_id+"?external_db=GO;all_levels=1"
        go_results=requests.get(server+ext,headers={ "Content-Type":"application/json"})
        if not go_results.ok:
            go_results.raise_for_status()
            sys.exit()
        decoded=go_results.json()
        if(decoded == []):
            print("\n[WARNING] There isn't any GO_entity in Gene Ontology database for the ensembl_ID: "+ensembl_id+".")
            continue
        else:
            output_dict[ensembl_id]=[]
            for go_entity_dict in decoded:
                if([go_entity_dict["display_id"]] not in output_dict[ensembl_id]):
                    output_dict[ensembl_id].append([go_entity_dict["display_id"]])
        for go_term in output_dict[ensembl_id]:
            ext_2="/ontology/id/"+go_term[0]+"?simple=1"
            go_results_2=requests.get(server+ext_2,headers={ "Content-Type":"application/json"})
            decoded_2=go_results_2.json()
            if("error" in decoded_2.keys()):
                print("\n[WARNING] for ensembl_ID: "+ensembl_id+" => "+str(decoded_2))
                output_dict[ensembl_id][output_dict[ensembl_id].index(go_term)].extend(['GO_term','NULL'])
            else:
                output_dict[ensembl_id][output_dict[ensembl_id].index([decoded_2["accession"]])].extend([decoded_2["namespace"],decoded_2["name"]])
        #i=len(output_dict[ensembl_id])-1
        #while(i>=0):
        #    if(len(output_dict[ensembl_id][i]) == 1):
        #        del output_dict[ensembl_id][i]
        #    i-=1
    if(output_dict != {}):
        GEN_DB_table_output_list=[]
        DB_table_output_list=[]
        for key in output_dict.keys():
            for value in output_dict[key]:
                GEN_DB_table_output_list.append([key,value[0]])
                if(value not in DB_table_output_list):
                    DB_table_output_list.append(value)
        GEN_DB_table_df=pd.DataFrame(GEN_DB_table_output_list,columns=["ensembl_gene_ID","database_ID"])
        display(GEN_DB_table_df)
        GEN_DB_table_selection=input("\nafter displayed GEN_DB table example do you want to save results in a .csv file in INPUT folder? (i.e. yes or not): ")
        if(GEN_DB_table_selection == "yes"):
            GEN_DB_table_df.to_csv(path_or_buf="./INPUT/"+name+"_"+surname+data+"_GEN_DB.csv",sep=",",header=True,index=False,na_rep="NULL")
        DB_table_df=pd.DataFrame(DB_table_output_list,columns=["database_ID","database_object_type","database_object_name"])
        display(DB_table_df)
        DB_table_selection=input("\nafter displayed DB table example do you want to save results in a .csv file in INPUT folder? (i.e. yes or not): ")
        if(DB_table_selection == "yes"):
            DB_table_df.to_csv(path_or_buf="./INPUT/"+name+"_"+surname+data+"_DB.csv",sep=",",header=True,index=False,na_rep="NULL")
        return("All done, thank you for processing Gene Ontology database data")
    else:
        return("Sorry, for the ensembl gene IDs list entered in input there isn't any output to create")