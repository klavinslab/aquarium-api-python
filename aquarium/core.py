import requests
import re
import json
import primer
import fragment


class AquariumAPI(object):
    def __init__(self, url, login, key, project=None):
        self.url = url
        self.login = login
        self.key = key
        self.project = project

        # Attempt a connection - tests the url, login, and key
        try:
            test_request = self._request({}, {})
        except requests.ConnectionError:
            raise requests.ConnectionError("Could not connect to URL")
        if test_request["result"] != "ok":
            raise requests.ConnectionError("{}".format(test_request["errors"]))

    def find(self, model, where_query=None):
        method = "find"
        run_data = {"model": model}
        if where_query is not None:
            run_data["where"] = where_query

        return self._request(method, run_data)

    def create(self, model, model_type, name, description, fields,
               project=None):
        if project is None:
            project = self.project
        method = "create"
        run_data = {"model": model, "type": model_type, "name": name,
                    "project": project, "description": description,
                    "fields": fields}

        return self._request(method, run_data)

    def submit_task(self, name_task, user_name_task, fields, project=None):
        if project is None:
            project = self.project
        json_task_prototype = self.find("task_prototype", {"name": name_task})
        task_prototype_id = json_task_prototype["rows"][0]["id"]

        method = "create"
        run_data = {"model": "task", "name": user_name_task,
                    "status": "waiting",
                    "task_prototype_id": task_prototype_id,
                    "specification": fields}

        return self._request(method, run_data)

    def drop_by_names(self, model, names):
        method = "drop"
        run_data = {"model": model, "names": names}

        return self._request(method, run_data)

    def drop_by_ids(self, model, ids):
        method = "drop"
        run_data = {"model": model, "ids": ids}

        return self._request(method, run_data)

    def modify(self, query_params):
        # TODO: Write once this is documented
        raise NotImplementedError("The 'modify' method has no API docs.")

    def _request(self, method, args):
        data = {}
        data["login"] = self.login
        data["key"] = self.key
        run = {"method": method, "args": args}
        data["run"] = run

        r = requests.post(self.url, json=data)
        # TODO: validate request error code
        if r.status_code != 200:
            print "Returned status code: %{}".format(r.status_code)
        else:
            json = r.json()
            # TODO: validate result ("status": OK)
            # TODO: provide a useful response message?
            return json
#############################################################    
    def get_ecoli_plate_id(self, plasmid_id):
        json_item=self.find("item", {"sample_id": plasmid_id})
        try: 
            return json_item["rows"][1]["id"]
        except:
            print "No E coli Plate of Plasmid "+str(plasmid_id)
            return None

    def sample_type_id(self, type):
        # input string (e.g. "Fragment" returns its sample_type_id
        json_sample_type_id = self.find("sample_type", {"Name": type})

        return json_sample_type_id["rows"][0]["id"]

    def find_sample_substring(self, type, regex_str_tofind):
        # find based on a substring in name or description

        json_res = self.find("sample",
                             {"sample_type_id": self.sample_type_id(type)})
        samples = []
        pattern = re.compile(regex_str_tofind)
        for i in json_res["rows"]:
            name_matches = pattern.search(json.dumps(i["name"]))
            description_matches = pattern.search(json.dumps(i["description"]))
            if name_matches or description_matches:
                samples.append(i)

        return samples

    def find_primers(self, overhang_seq="", anneal_seq="", name=""):
        primers = []
        for i in self.find("sample",
                           {"sample_type_id": self.sample_type_id("Primer")}
                           )["rows"]:
            name_match=i["name"] == name
            overhang_match = i["fields"]["Overhang Sequence"] == str(overhang_seq)
            anneal_match = i["fields"]["Anneal Sequence"] == str(anneal_seq)
            if (overhang_match and anneal_match) or name_match:
                primers.append(i)
        return primers    
    
    
    def find_bacterial_marker(self, plasmid_name):
        bacterial_marker=""

        for i in self.find("sample",
                           {"sample_type_id": self.sample_type_id("Plasmid")}
                           )["rows"]:
            name_match=i["name"] == plasmid_name
            
            if name_match:
                bacterial_marker=i["fields"]["Bacterial Marker"]
                break
        return bacterial_marker     
    
    def find_yeast_marker(self, plasmid_name):
        yeast_marker=""

        for i in self.find("sample",
                           {"sample_type_id": self.sample_type_id("Plasmid")}
                           )["rows"]:
            name_match=i["name"] == plasmid_name
            
            if name_match:
                yeast_marker=i["fields"]["Yeast Marker"]
                break
        return yeast_marker    
    
    def find_yeast_strain_id(self, strain_name):
        for i in self.find("sample",
                           {"sample_type_id": self.sample_type_id("Yeast Strain"), 
                            "name": strain_name}
                           )["rows"]:
            id = i["id"] 

        return id
    
    def find_plasmid_id(self, plasmid_name):
        id=0
        for i in self.find("sample",
                           {"sample_type_id": self.sample_type_id("Plasmid"), 
                            "name": plasmid_name}
                           )["rows"]:
            id = i["id"] 

        if id !=0:    
            return id
        else:
            print plasmid_name+" not found in Aquarium"
            return False
    
    def find_yeast_fragment_id(self, fragment_name):
        id=0

        for i in self.find("sample",
                           {"sample_type_id": self.sample_type_id("Fragment"), 
                            "name": fragment_name}
                           )["rows"]:
            id = i["id"]
        if id !=0:    
            return id
        else:
            print fragment_name+" not found in Aquarium"
            return False

    def get_primer(self, name):
        primers=[] 
        for i in self.find("sample",
                           {"sample_type_id": self.sample_type_id("Primer"), 
                            "name": name}
                           )["rows"]:
            primers.append(primer.primer(name, 
                                  i["description"], 
                                  i["fields"]["Overhang Sequence"], 
                                  i["fields"]["Anneal Sequence"], 
                                  i["fields"]["T Anneal"]
                                  )
                           ) 
        if len(primers) == 1:
            return primers[0]
        else:
            print "Error finding your primer"
            return None   
        
           
    def get_fragment(self, fragment_name):
        f=[]
        for i in self.find("sample",
                           {"sample_type_id": self.sample_type_id("Fragment"), 
                            "name": fragment_name}
                           )["rows"]:
            f=i
            break
        #not implemented the marker (because come back as None, restriction enzyme, nor seq_url
        print fragment_name
        print f
        fwd_primer=self.get_primer(f["fields"]["Forward Primer"])
        if not fwd_primer:
            fwd_primer=primer.primer('none', 'placeholder primer', '', '', 0)
        rev_primer=self.get_primer(f["fields"]["Reverse Primer"])
        if not rev_primer:
            rev_primer=primer.primer('none', 'placeholder primer', '', '', 0)
            
        if f:
            print "Fragment "+f["name"]+" found with id="+str(f["id"])
            return fragment.fragment(f["name"], 
                            f["description"], 
                            f["fields"]["Length"], 
                            f["fields"]["Template"], 
                            fwd_primer, 
                            rev_primer)   
        else:
            print "Error finding your fragment "+fragment_name
            return None 
        
    def get_fragment_sequence(self, fragment_name):
        f=[]
        for i in self.find("sample",
                           {"sample_type_id": self.sample_type_id("Fragment"), 
                            "name": fragment_name}
                           )["rows"]:
            f=i

        if f:
            return f["fields"]["Sequence"]  
        else:
            return None 
            