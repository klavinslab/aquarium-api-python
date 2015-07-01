'''
Created on May 19, 2015

@author: laura
'''
import json

class yeast_strain():
    
    def __init__(self, name, description, parent="", integrant="", plasmid="", integrated_marker="", plasmid_marker="", mating_type="", qc_primer1="", qc_primer2=""):
        #Description: A linear double stranded piece of DNA from PCR or Restriction Digest
        #Parent: Yeast strain
        #Integrant: Plasmid|Fragment
        #Plasmid: Plasmid
        #Integrated Marker(s): string
        #Plasmid Marker(s): string
        #Mating Type: string
        #QC Primer1: Primer
        #QC Primer2: Primer
        
        self.name=name
        self.description=description 
        self.parent=parent
        self.integrant=integrant
        self.plasmid=plasmid
        self.integrated_marker=integrated_marker
        self.plasmid_marker=plasmid_marker
        self.mating_type=mating_type
        self.qc_primer1=qc_primer1
        self.qc_primer2=qc_primer2

        
    def __str__(self):
        return self.name

    def aquariumify(self, conn):
        
        #is it in Aq already?
        json_fragment=conn.find("sample", {"sample_type_id": conn.sample_type_id("Yeast Strain"), "name": self.name})
        if json_fragment["rows"]:
            yeast_id=json_fragment["rows"][0]["id"]
            print "I found your yeast strain!"
            print json_fragment["rows"][0]
                
        else:
            print "Creating Aquarium Entry for yeast strain:"            
            params={}#empty json
            if self.parent is not "":
                params["Parent"]=int(self.parent)
            if self.integrant is not "":
                params["Integrant"]=int(self.integrant)
            if self.plasmid is not "":
                params["Plasmid"]=int(self.plasmid)
            if self.integrated_marker is not "":
                params["Integrated Marker(s)"]=self.integrated_marker
            if self.plasmid_marker is not "":
                params["Plasmid Marker(s)"]=self.plasmid_marker
            if self.mating_type is not "":
                params["Mating Type"]=self.mating_type
            if self.qc_primer1 is not "":
                params["QC Primer1 Primer"]=int(self.qc_primer1)
            if self.qc_primer2 is not "":
                params["QC Primer2 Primer"]=int(self.qc_primer2)
                
            print params
                                
            json_fragment= conn.create("sample", 
                                            "Yeast Strain", 
                                            self.name, 
                                            self.description, 
                                            params
                                        )
            print json_fragment
            yeast_id=json_fragment["rows"][0]["id"]
            
        return yeast_id
    
    def check_yeast_stock(self, conn, yeast_id):
        #should we use on in stock, if any?

        in_stock=conn.find("item", {"sample_id": yeast_id, "quantity": 1}) 
        if in_stock["rows"]:
            print "I found the following record(s) of your yeast in stock! :" 
            for idx, val in enumerate(in_stock["rows"]):  
                print idx, val             
            which_stock_item = input("Do you want to use any of the following fragment(s) or make a new one? (enter number -else- any letters) : ")      
            if isinstance(which_stock_item, int):
                print "There is nothing to do for me. Use yeast id %d, item %d" %(yeast_id,in_stock["rows"][which_stock_item]["id"])
                return in_stock["rows"][which_stock_item]["id"]
        else:
            #do nothing 
            print "The yeast is not in stock!"
            return False
    
    def make_it_aquarium(self, conn, strain_id):
        if not self.check_yeast_stock(conn, strain_id):
                
            status= conn.submit_task("Yeast Transformation", 
                                    "Transformation of "+self.name, 
                                    {"yeast_transformed_strain_ids Yeast Strain": [strain_id]}
                                    )
            print "DONE! Task 'Yeast Transformation' should be created:"
            print status
            return status
        else:
            print "Yeast already in stock !"