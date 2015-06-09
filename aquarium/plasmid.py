'''
Created on Jun 3, 2015

@author: laura
'''
class plasmid():
    
    def __init__(self, name, description, sequence, bacterial_marker, yeast_marker, length, sequencing_primer_ids="N/A",sequence_verification=""):
        """
        Description: A circular piece of double stranded DNA
        Sequence: url
        Sequence Verification: url
        Bacterial Marker: string
        Yeast Marker: string
        Length: number
        Sequencing_primer_ids: string
        """
        
        self.name=name
        self.description=description 
        self.sequence=sequence
        self.sequence_verification=sequence_verification
        self.bacterial_marker=bacterial_marker 
        self.yeast_marker=yeast_marker
        self.length=length 
        self.sequencing_primer_ids=sequencing_primer_ids
        
    def __str__(self):
        return self.name 
           
    def aquariumify(self, conn):
        #does it already exist?
        plasmid_id=conn.find_plasmid_id(self.name)
        
        if not plasmid_id:
            #create new plasmid
            print "Now, we are creating the plasmid record."
                    
            json_plasmid= conn.create("sample",
                                      "Plasmid",
                                      self.name,
                                      self.description, 
                                      {"Sequence": self.sequence,
                                       "Length": self.length,
                                       "Sequence Verification": self.sequence_verification,
                                       "Bacterial Marker": self.bacterial_marker,
                                       "Yeast Marker": self.yeast_marker,
                                       "Sequencing_primer_ids": self.sequencing_primer_ids
                                       }
                                       )
            print json_plasmid
            plasmid_id=json_plasmid["rows"][0]["id"]
        else:
            print "Plasmid "+self.name+" already in Aquarium!"
             
        return plasmid_id     
        
    def make_it_aquarium(self, conn, list_fragments_id):
        plasmid_id=self.aquariumify(conn)
        print conn.submit_task("Gibson Assembly", 
                                    "Gibson Assembly of "+self.name, 
                                    {"fragments": list_fragments_id,
                                     "plasmid": plasmid_id
                                     }
                                    )