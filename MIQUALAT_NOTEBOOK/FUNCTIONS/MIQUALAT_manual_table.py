#relational table
#NULL value check and empty for auto-NULL

def relational_table():
    integer_progressive_ID="NULL"
    pubmed_ID=input("enter pubmed_ID (ex 29680643), cannot be NULL (empty): ")
    while pubmed_ID == "" or pubmed_ID.lower() == "null":
        print ("pubmed_ID cannot be NULL retry")
        pubmed_ID=input("enter pubmed_ID (ex 29680643), cannot be NULL (empty): ")
    ensembl_gene_ID=input("enter ensembl_gene_ID (ex ENSBTAG00000031544), can be NULL (empty), insert one at time: ")
    if ensembl_gene_ID == "" or ensembl_gene_ID.lower() == "null":
        ensembl_gene_ID = "NULL"
    variant_name=input("enter variant_name (NULL or variant_name, variant table for more info), can be NULL (empty): ")
    if variant_name == "" or variant_name.lower() == "null":
        variant_name = "NULL"
    tecnique=input("enter tecnique (ex QPCR), can be NULL (empty): ")
    if tecnique == "" or tecnique.lower() == "null":
        tecnique = "NULL"
    #see for i cicle
    keyword_tags=input("enter keyword_tags (ex apoptosis, antioxidants), insert one keyword at time, can be NULL (empty): ")
    relationship_note=input("enter relationship_note (simple description of relationship max 200 char ex gene and tecnique), can be NULL (empty): ")
    if relationship_note == "" or relationship_note.lower() == "null":
        relationship_note = "NULL"
    integer_progressive_ID=('"'+integer_progressive_ID+'"').replace(" ","")
    pubmed_ID=('"'+pubmed_ID+'"').replace(" ","")
    ensembl_gene_ID=('"'+ensembl_gene_ID+'"').replace(" ","")
    variant_name=('"'+variant_name+'"')
    tecnique=('"'+tecnique+'"')
    relationship_note='"'+relationship_note+'"'
    keyword_tags=keyword_tags.split(",")
    for i in keyword_tags:
        if i == "" or i.lower() == "null":
            i = "NULL"
        i=('"'+i+'"')
        table_file=open("PUB_GEN_VAR_TEC_TAG.csv","a")
        table_file.write(integer_progressive_ID+','+pubmed_ID+','+\
                              ensembl_gene_ID+','+variant_name+','+\
                              tecnique+','+i+','+relationship_note+'\n')

def relational_table_repeat():
    repeat=True
    while repeat:
        choice = input("enter yes to continue insertion, or leave empty for exit (file will be saved): ")
        if choice != "yes":
            print("\nsee you later!")
            repeat=False
        else:
            relational_table()  

#relational table more genes at a time

def relational_table_list_of_gene():
	integer_progressive_ID="NULL"
	pubmed_ID=input("enter pubmed_ID (ex 29680643), cannot be NULL (empty): ")
	while pubmed_ID == "" or pubmed_ID.lower() == "null":
		print ("pubmed_ID cannot be NULL retry")
		pubmed_ID=input("enter pubmed_ID (ex 29680643), cannot be NULL (empty): ")
	ensembl_gene_ID=input("enter ensembl_gene_ID (ex ENSBTAG00000031544,ENSBTAG00000053003), can be NULL (empty): ")
	ensembl_gene_ID=ensembl_gene_ID.split(",")
	ensembl_gene_ID=["NULL" if i=="" else i for i in ensembl_gene_ID]
	ensembl_gene_ID=["NULL" if i.lower()=="null" else i for i in ensembl_gene_ID]
	variant_name=input("enter variant_name (NULL or variant_name, variant table for more info), can be NULL (empty): ")
	if variant_name == "" or variant_name.lower() == "null":
		variant_name = "NULL"
	tecnique=input("enter tecnique (ex QPCR), can be NULL (empty): ")
	if tecnique == "" or tecnique.lower() == "null":
		tecnique = "NULL"
	#see for i cicle
	keyword_tags=input("enter keyword_tags (ex apoptosis, antioxidants), insert one keyword at time, can be NULL (empty): ")
	relationship_note=input("enter relationship_note (simple description of relationship max 200 char ex gene and tecnique), can be NULL (empty): ")
	if relationship_note == "" or relationship_note.lower() == "null":
		relationship_note = "NULL"
	integer_progressive_ID=('"'+integer_progressive_ID+'"').replace(" ","")
	pubmed_ID=('"'+pubmed_ID+'"').replace(" ","")
	variant_name=('"'+variant_name+'"')
	tecnique=('"'+tecnique+'"')
	relationship_note='"'+relationship_note+'"'
	keyword_tags=keyword_tags.split(",")
	for i in keyword_tags:
		if i == "" or i.lower() == "null":
			i = "NULL"
		i=('"'+i+'"')
		table_file=open("PUB_GEN_VAR_TEC_TAG.csv","a")
		for x in ensembl_gene_ID:
			x=('"'+x+'"').replace(" ","")
			table_file.write(integer_progressive_ID+','+pubmed_ID+','+\
								  x+','+variant_name+','+\
								  tecnique+','+i+','+relationship_note+'\n')            

#tag table
  
def tag_table():
    keyword_tags=input("enter keyword_tags (ex antioxidants), cannot be NULL (empty): ")
    while keyword_tags == "" or keyword_tags.lower() == "null":
        print ("keyword_tags cannot be NULL retry")
        keyword_tags=input("enter keyword_tags (ex antioxidants), cannot be NULL (empty): ")
    tags_short_description=input("enter tags_short_description (ex prevent or slow damage to cells caused by free radicals), cannot be NULL (empty): ")
    while tags_short_description == "" or tags_short_description.lower() == "null":
        print ("tags_short_description cannot be NULL retry")
        tags_short_description=input("enter tags_short_description (ex prevent or slow damage to cells caused by free radicals), cannot be NULL (empty): ")
    keyword_tags=('"'+keyword_tags+'"') 
    tags_short_description=('"'+tags_short_description+'"')   
    table_file=open("TAG.csv","a")
    table_file.write(keyword_tags+','+tags_short_description+"\n")


def tag_table_repeat():
    repeat=True
    while repeat:
        choice = input("enter yes to continue insertion, or leave empty for exit (file will be saved): ")
        if choice != "yes":
            print("\nsee you later!")
            repeat=False
        else:
            tag_table()  

#tecnique table
def tecnique_table():
    tecnique=input("enter tecnique (ex QPCR), cannot be NULL (empty): : ")
    while tecnique == "" or tecnique.lower() == "null":
        print ("tecnique cannot be NULL retry")
        tecnique=input("enter tecnique (ex QPCR), cannot be NULL (empty): : ")
    tecnique_short_description=input("enter tecnique_short_description (ex quantitative polymerase chain reaction), cannot be NULL (empty): ")
    while tecnique_short_description == "" or tecnique_short_description.lower() == "null":
        print ("tecnique_short_description cannot be NULL retry")
        tecnique_short_description=input("enter tecnique_short_description (ex quantitative polymerase chain reaction), cannot be NULL (empty): ")    
    tecnique='"'+tecnique+'"'    
    tecnique_short_description='"'+tecnique_short_description+'"'    
    table_file=open("TECNIQUE.csv","a")
    table_file.write(tecnique+','+tecnique_short_description+"\n")

def tecnique_table_repeat():
    repeat=True
    while repeat:
        choice = input("enter yes to continue insertion, or leave empty for exit (file will be saved): ")
        if choice != "yes":
            print("\nsee you later!")
            repeat=False
        else:
            tecnique_table()  

#variant table

def variant_table():
    variant_name=input("enter variant_name, cannot be NULL (empty): ")
    while variant_name == "" or variant_name.lower() == "null":
        print ("variant_name cannot be NULL retry")
        variant_name=input("enter variant_name, cannot be NULL (empty): ")
    variant_type=input("enter variant_type, cannot be NULL (empty): ")
    while variant_type == "" or variant_type.lower() == "null":
        print ("variant_type cannot be NULL retry")
        variant_type=input("enter variant_type, cannot be NULL (empty): ")
    chromosome=input("enter chromosome, cannot be NULL (empty): ")
    while chromosome == "" or chromosome.lower() == "null":
        print ("chromosome cannot be NULL retry")
        chromosome=input("enter chromosome, cannot be NULL (empty): ")
    position=input("enter position, cannot be NULL (empty): ")
    while position == "" or position.lower() == "null":
        print ("position cannot be NULL retry")
        position=input("enter position, cannot be NULL (empty): ")            
    reference_allele=input("enter reference_allele, cannot be NULL (empty): ")
    while reference_allele == "" or reference_allele.lower() == "null":
        print ("reference_allele cannot be NULL retry")
        reference_allele=input("enter reference_allele, cannot be NULL (empty): ")
    alternative_allele=input("enter alternative_allele, cannot be NULL (empty): ")
    while alternative_allele == "" or alternative_allele.lower() == "null":
        print ("alternative_allele cannot be NULL retry")
        alternative_allele=input("enter alternative_allele, cannot be NULL (empty): ")
    rs_ID=input("enter rs_ID, can be NULL (empty): ")
    if rs_ID == "" or rs_ID.lower() == "null":
        rs_ID="NULL"
    species=input("enter species, cannot be NULL (empty): ")
    while species == "" or species.lower() == "null":
        print ("species cannot be NULL retry")
        species=input("enter species, cannot be NULL (empty): ")
    refseq=input("enter refseq, cannot be NULL (empty): ")
    while refseq == "" or refseq.lower() == "null":
        print ("refseq cannot be NULL retry")
        refseq=input("enter refseq, cannot be NULL (empty): ")
   
   
    variant_name='"'+variant_name+'"'
    variant_type='"'+variant_type+'"'
    chromosome='"'+chromosome+'"'
    position='"'+position+'"'
    reference_allele='"'+reference_allele+'"' 
    alternative_allele='"'+alternative_allele+'"'
    rs_ID='"'+rs_ID+'"'  
    species='"'+species+'"'      
    refseq='"'+refseq+'"'
    
    table_file=open("VARIANT.csv","a")
    table_file.write(variant_name+','+variant_type+','+chromosome+','+position+\
                          ','+reference_allele+','+alternative_allele+rs_ID+species+refseq+"\n")

def variant_table_repeat():
    repeat=True
    while repeat:
        choice = input("enter yes to continue insertion, or leave empty for exit (file will be saved): ")
        if choice != "yes":
            print("\nsee you later!")
            repeat=False
        else:
            variant_table()  
