'''
Created on May 14, 2015

@author: laura
'''
import core
import pymbt

class primer():
    
    def __init__(self, name, description, overhang_seq, anneal_seq, t_anneal):
        #Description: A short double stranded piece of DNA for PCR and sequencing
        #Overhang Sequence: string
        #Anneal Sequence: string
        #T Anneal: int
        self.name=name
        self.description=description  
        self.overhang_seq=overhang_seq 
        self.anneal_seq=anneal_seq     
        self.t_anneal=t_anneal
        
    def pymbtify(self):
        return pymbt.Primer(pymbt.DNA(self.anneal_seq), self.t_anneal, pymbt.DNA(self.overhang_seq), self.name, self.description)

    def save(self, filename):
        with open(filename, "a+") as myfile:
            myfile.write("primer("+self.fwd_primer.name+", "+self.fwd_primer.description+", "+self.fwd_primer.overhang_seq+", "+self.fwd_primer.anneal_seq+", "+self.fwd_primer.t_anneal+")")          
      
        
    def aquariumify(self, conn):
        #left_primer
        has_primer=conn.find_primers(self.overhang_seq,self.anneal_seq, self.name)
        if has_primer:
            print "Primer is already in Aquarium! We'll proceed with: "
            print has_primer
            primer_id=has_primer[0]["id"]
        else:
            #create primer
            json= conn.create("sample",
                              "Primer",
                              self.name,
                              self.description,
                              {"Overhang Sequence": self.overhang_seq,
                               "Anneal Sequence": self.anneal_seq,
                               "T Anneal": self.t_anneal}
                              )
            print json
            primer_id=json["rows"][0]["id"]   
            
            #order it
            print conn.submit_task("Primer Order","Primer Order of "+self.name, 
                                    {"primer_ids": [primer_id]
                                     }
                                    )
               
        return primer_id
