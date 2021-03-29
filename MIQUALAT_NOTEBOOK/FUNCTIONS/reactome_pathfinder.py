from reactome2py import content
import pandas as pd
from IPython.display import display
import datetime

def reactome_pathfinder():
    name=input("Enter your name: ")
    surname=input("Enter your surname: ")
    data = datetime.datetime.now()
    data = ("_" + str(data.year) + "-" + str(data.month) + "-" + \
            str(data.day) + "_" + str( int (data.hour)) + "-" + \
            str(data.minute) + "-" + str(data.second))
    print("[INFO] the function reactome_pathfinder() retrieves reactome database pathways code/ID and other informations on all the pathways related to a gene ENSEMBL_ID or a list of gene ENSEMBL_IDs")
    species=input("\nPlease enter only one species to perform the research [i.e. Bos taurus or Ovis aries or others]: ")
    ensembl_id_list=input("\nPlease enter a gene ENSEMBL_ID or a list of gene ENSEMBL_IDS comma separated [i.e. ENSBTAG00000012023 or ENSBTAG00000012023,ENSBTAG00000014486,...,ENSBTAG00000016484]:").split(',')
    output_dict={}
    for ensembl_id in ensembl_id_list:
        pathways_repository=content.mapping(id=ensembl_id, resource='ENSEMBL', species=species, by='pathways')
        if(pathways_repository is None):
            print("\n[WARNING] There isn't any pathway in reactome database for the ensembl_ID: "+ensembl_id+".")
        else:
            output_dict[ensembl_id]=[]
            for pathway_dict in pathways_repository:
                output_dict[ensembl_id].append([pathway_dict["stId"],"reactome_pathway",pathway_dict["displayName"]])
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
        return("All done, thank you for processing reactome database data")
    else:
        return("Sorry, for the ensembl gene IDs list entered in input there isn't any output to create")
    