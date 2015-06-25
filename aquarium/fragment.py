'''
Created on May 14, 2015

@author: laura
'''


class fragment():
    
    def __init__(self, name, description, length, template, fwd_primer, rev_primer, seq_url="N/A", marker=""):
        #Description: A linear double stranded piece of DNA from PCR or Restriction Digest
        #Sequence: url
        #Length: number
        #Template: Plasmid|E coli strain|Fragment|Yeast Strain
        #Forward Primer: Primer
        #Reverse Primer: Primer
        #Restriction Enzyme(s): string
        
        self.name=name
        self.description=description 
        self.seq_url=seq_url 
        self.length=length 
        self.template=template
        self.fwd_primer=fwd_primer
        self.rev_primer=rev_primer
        self.marker=marker
        
    def __str__(self):
        return self.name
    
    def save(self, filename):
        self.fwd_primer.save(filename)
        self.rev_primer.save(filename)
        with open(filename, "a+") as myfile:
            myfile.write("fragment("+self.name+", "+self.description+", "+self.length+", "+self.template+", "+self.fwd_primer+", "+self.rev_primer+", "+self.seq_url+", "+self.marker+")")
        
        
    
    def aquariumify(self, conn):
        
        #is it in Aq already?
        json_fragment=conn.find("sample", {"sample_type_id": conn.sample_type_id("Fragment"), "name": self.name})
        if json_fragment["rows"]:
            fragment_id=json_fragment["rows"][0]["id"]
            print "I found your fragment!"
            print json_fragment["rows"][0]
                
        else:
            
            #is there a similar one?
            aq_my_fragment=conn.find_sample_substring("Fragment", "(.*"+self.name+")")
            if aq_my_fragment:
                print "Your fragment may already exists! I found the following record(s):"
                for idx, val in enumerate(aq_my_fragment): 
                    print idx, val
                which_fragment = input("Would you like to use one of these fragments? (enter number -else- any letters) : ")          
                if isinstance(which_fragment, int):
                    #we already know which Fragement
                    fragment_id=aq_my_fragment[which_fragment]["id"]
                    if not self.check_fragment_stock(conn, fragment_id):
                        self.create_fragment_construction(conn, self.name, fragment_id)     
            else:
                
                #fragment design
                print "Let's create the Primers records first."               
                
                fwd_primer_aq_id=self.fwd_primer.aquariumify(conn)
                rev_primer_aq_id=self.rev_primer.aquariumify(conn)

                #create new fragment
                print "Now, we are creating the fragment record."
                
                json_fragment= conn.create("sample", 
                                            "Fragment", 
                                            self.name, 
                                            self.description, 
                                            {  "Sequence": self.seq_url,
                                            "Length": self.length,
                                            "Template": self.template,
                                            "Forward Primer": int(fwd_primer_aq_id),
                                            "Reverse Primer": int(rev_primer_aq_id),
                                            "Restriction Enzyme(s)":"",
                                            "Yeast Marker": self.marker
                                            }
                                            )
                print json_fragment
                fragment_id=json_fragment["rows"][0]["id"]
        
        
        return fragment_id
    
    def make_it_aquarium(self, conn, fragment_id):
        #create Fragment construction task in Aquarium
        print "/!\ not checking for yeast lysate...."
        self.create_fragment_construction(conn, fragment_id)

            
    def check_fragment_stock(self, conn, fragment_id):
        #should we use on in stock, if any?

        in_stock=conn.find("item", {"sample_id": fragment_id, "quantity": 1}) 
        if in_stock["rows"]:
            print "I found the following record(s) of your fragment in stock! :" 
            for idx, val in enumerate(in_stock["rows"]):  
                print idx, val             
            which_stock_item = input("Do you want to use any of the following fragment(s) or make a new one? (enter number -else- any letters) : ")      
            if isinstance(which_stock_item, int):
                print "There is nothing to do for me. Use fragment id %d, item %d" %(fragment_id,in_stock["rows"][which_stock_item]["id"])
                return in_stock["rows"][which_stock_item]["id"]
        else:
            #do nothing 
            print "The fragment is not in stock!"
            return False
            
    def create_fragment_construction(self, conn, fragment_id):
        if not self.check_fragment_stock(conn, fragment_id):
                
            status= conn.submit_task("Fragment Construction", 
                                    "Construction of "+self.name, 
                                    {"fragments Fragment": [fragment_id]}
                                    )
            print "DONE! Task 'Fragment construction' should be created:"
            print status
            return status
        else:
            print "Fragment already in stock !"
            
