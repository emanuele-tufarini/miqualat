'''
emanuele.tufarini@live.com
last modification 11-2020
'''

# import modules
import os, re, datetime
from Bio import Entrez, Medline
Entrez.email = input("insert your e-mail: ") 

def pubmed_search(keyword,keyword_title):

    name = input ("Enter your name: ") 
    surname = input ("Enter your surname: ") 
    data = datetime.datetime.now()
    data = ("_" + str(data.year) + "-" + str(data.month) + "-" + \
            str(data.day) + "_" + str( int (data.hour)) + "-" + \
            str(data.minute) + "-" + str(data.second))
    print("\n")
    
    PUBMED_SEARCH_FILE_NAME = name + "_" + surname + "_" +  str(data) + "_PUBMED_SEARCH" + ".txt"
    PUBMED_SEARCH=open(PUBMED_SEARCH_FILE_NAME,"w")
    PUBMED_SEARCH.write(keyword+"\n"+keyword_title+"\n\n")
    PUBMED_SEARCH=open(PUBMED_SEARCH_FILE_NAME,"a")
    
    keyword = "(" + keyword.lower() + ")"
    keyword_title = "(" + keyword_title.lower() + ")"
    # set up PubMed as a database
    handle = Entrez.esearch(db="pubmed", term=keyword + keyword_title)
    record = Entrez.read(handle)
    pmids = record['IdList']
    handle = Entrez.efetch(db="pubmed", id=pmids,
                           rettype="medline", retmode="text")
    medline_records = Medline.parse(handle)
    records = list(medline_records)
    n = 1
    print("keyword in articles: " + keyword)
    print("keyword in titles: " + keyword_title + "\n")
    # returns all articles that have the keyword_title in title
    try:
        for record in records:
            # variables to print
            RESULT = ("RESULT " + str (n))
            TITLE = ((str(record["TI"]).replace('"', "'")).replace("'", ""))
            PMID = (record["PMID"])
            AUTHORS = ((((str(record["AU"]).replace("[", "")).replace("]", "")).replace('"', "")).replace("'", ""))
            JOURNAL = (record["TA"])
            DATA = (record["DP"][:4]) #yyy/mm/dd
            URL = ("https://www.ncbi.nlm.nih.gov/pubmed/?term=" + PMID)
            # se non e' riportato il doi, inserisci una stringa vuota
            try:
                AID = ((str(record["AID"]).replace('"', "'")).replace("'", "")) # article identifier
                AID = AID.split (",")
                DOI = [i for i in AID if "doi" in i]
                DOI = (str (DOI)).replace('[doi]', "").replace("[", "").replace("]", "").replace(" ", "").replace("'", "")
            except:
                DOI = "NULL"
                pass
            
            # print results
            print (RESULT,
            "| TITLE | " + TITLE,
            "| PMID | " + PMID,
            "| DOI | " + DOI,
            "| AUTHORS | " + AUTHORS,
            "| JOURNAL | " + JOURNAL,
            "| DATA | " + DATA,
            "| URL | "+ URL + "\n")
            # write result
            PUBMED_SEARCH.write(RESULT+
            "| TITLE | " + str(TITLE)+
            "| PMID | " + str(PMID)+
            "| DOI | " + str (DOI)+     
            "| AUTHORS | " + str(AUTHORS)+
            "| JOURNAL | " + str(JOURNAL)+
            "| DATA | " + str(DATA)+
            "| URL | "+ str(URL) + "\n\n")
            n = n + 1
                       
    except:
        pass
    # create a pmids dictionary
    DizPMID = {}
    n = 1
    try:
        for record in records:
            DizPMID[n] = record["PMID"]
            n += 1
    except:
        pass
    print("\nenter 'exit' for quit or leave empty\n")
    NumArticle = (input("enter the title number for print the article/s (1,2,3,4,5 .. ): ")).replace(" ", "")
    if NumArticle == "exit":
        print("\nsee you later!")
    else:
        ListNum = re.split(",", NumArticle)
        # write selected articles
        PUBLICATION_CSV = open (name + "_" + surname + "_" +  str(data) + "_PUBLICATION" + ".csv", "w")
        PUBLICATION_CSV.write("pubmed_ID,doi,article_title,article_authors,article_journal,publication_year\n")
        for Num in ListNum:
            try:
                PUBLICATION_CSV = open (name + "_" + surname + "_" +  str(data) + "_PUBLICATION.csv", "a")
                for PMID in DizPMID:
                    for record in records:
                        if DizPMID[int(Num)] in record["PMID"]:
                            # variables to print
                            RESULT = ("RESULT " + str (Num))
                            TITLE = ((str(record["TI"]).replace('"', "'")).replace("'", ""))
                            PMID = (record["PMID"])
                            AUTHORS = ((((str(record["AU"]).replace("[", "")).replace("]", "")).replace('"', "")).replace("'", ""))
                            JOURNAL = (record["TA"])
                            DATA = (record["DP"][:4]) #yyy/mm/dd
                            URL = ("https://www.ncbi.nlm.nih.gov/pubmed/?term=" + PMID)
                            # write the results to the PUBLICATION.csv
                            PUBLICATION_CSV.write ('"' + str(PMID) + '","' + str(DOI) + '","' + str (TITLE) + '","' + str(AUTHORS) + '","' + str(JOURNAL) + '","' + str(DATA) + '"\n')
                    break
                PUBLICATION_CSV.close()
                print ("article",Num,"has been written .. all done ..")
            except:
                print("article ",Num," not found, are aviable ",len(DizPMID.keys())," article/s")
        PUBMED_SEARCH.close()
        print("\nsee you later!")
        
