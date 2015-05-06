import requests
import re
import json


class AquariumAPI(object):
    def __init__(self, url, login, key, project=None):
        self.url = url
        self.login = login
        self.key = key
        self.project = project

        # TODO: Attempt a connection - test the url and key

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
    
    #####################################
    ###########
    ########### this section should be seperated from this file
    ###########
    
    def sample_type_id(self, type):
        #input string (e.g. "Fragment" returns its sample_type_id
        json_sample_type_id=self.find("sample_type",{"Name": type})
        
        return json_sample_type_id["rows"][0]["id"]
    
    def find_sample_substring(self, type, regex_str_tofind):
        #find based on a substring in name or description
        
        json_res=self.find("sample", 
                           {"sample_type_id": self.sample_type_id(type)})        
        samples=[]
        pattern=re.compile(regex_str_tofind)
        for i in json_res["rows"]:
            if (pattern.search(json.dumps(i["name"])) or 
                pattern.search(json.dumps(i["description"]))):
            #if sub_name in i["name"]:
                #print i
                samples.append(i)
                
        return samples
    
    def find_primers(self, overhang_seq, anneal_seq):
        primers=[]
        for i in self.find("sample", 
                           {"sample_type_id": self.sample_type_id("Primer")}
                           )["rows"]:
            if ((i["fields"]["Overhang Sequence"] == overhang_seq) and 
                (i["fields"]["Anneal Sequence"] == anneal_seq)) :
                primers.append(i)
        return primers    
        
    ###########
    ##################################### 

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