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
        self.standard_name=self.name+"("+self.bacterial_marker+"|"+self.yeast_marker+")"
        
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
                                    {"fragments Fragment": list_fragments_id,
                                     "plasmid Plasmid": plasmid_id
                                     }
                                    )
        
    def verify_it_aquarium(self, conn, list_primers_id, num_colonies):
        plasmid_id=self.aquariumify(conn)
        plate_id=conn.get_ecoli_plate_id(plasmid_id)             
        print conn.submit_task("Plasmid Verification", 
                                    "Plasmid Verification:: "+self.name, 
                                    {"plate_ids E coli Plate of Plasmid": [plate_id],
                                     "num_colonies": [num_colonies],
                                     "primer_ids Primer": [list_primers_id],
                                     "initials": conn.login[:2]                       
                                     }
                                    )
        