import requests


class AquariumAPI(object):
    '''Reusable Aquarium API connector.'''
    def __init__(self, url, login, key):
        '''
        :param url: URL of the API, usually (aquarium base URL)/api.
        :type url: str
        :param login: Aquarium user login name.
        :type login: str
        :param key: Aquarium API key.
        :type key: str

        '''
        self.url = url
        self.login = login
        self.key = key

        # Attempt a connection - tests the url, login, and key
        try:
            test_request = self._request({}, {})
        except requests.ConnectionError:
            raise requests.ConnectionError('Could not connect to URL')
        if test_request['result'] != 'ok':
            raise requests.ConnectionError('{}'.format(test_request['errors']))

    def find(self, model, where=None, limit=None):
        '''Find entries in a model matching a query on table columns.

        :param model: Model in the database to search.
        :type model: str
        :param where: A query of column: comparator key-value pairs,
                            e.g. {'id': 5}
        :type where: dict
        :param limit: Limits the number of queries to return (synonymous with
                     SQL LIMIT).
        :type limit: int

        '''
        method = 'find'
        run_args = {'model': model}
        if where is not None:
            run_args['where'] = where
        if limit is not None:
            run_args['limit'] = limit

        return self._request(method, run_args)

    def create_sample(self, sample_type, name, description, fields, project):
        '''Create a new sample (adds new row to Sample table).

        :param sample_type: The name of the 'SampleType', e.g. 'PCR' or
                            'Fragment'.
        :type sample_type: str
        :param name: Name of the new database entry (e.g. a primer name).
        :type name: str
        :param description: A description of the new entry.
        :param name: str
        :param fields: Named fields that must be completed for this model, e.g.
                       {'Anneal Sequence': 'GACGATCGAGCGATCAT'}
        :type fields: dict
        :param project: Aquarium project with which to associate this
                        submission.
        :type project: str

        '''
        method = 'create'
        run_args = {'model': 'sample', 'type': sample_type, 'name': name,
                    'project': project, 'description': description,
                    'fields': fields}

        return self._request(method, run_args)

    def create_task(self, name, task_type, specification):
        '''Creates a new task (adds new row to Tasks table).

        :param name_task: Task type name (e.g. 'PCR')
        :type name_task: str
        :param user_name_task: Name of the task instance (e.g. 'My plasmid').
        :type user_name_task: str
        :param fields: key-value pairs of fields that need to be filled for
                       the task.
        :type fields: dict
        :param project: Aquarium project with which to associate this
                        submission.
        :type project: str

        '''
        json_task_prototype = self.find('task_prototype', {'name': task_type})
        task_prototype_id = json_task_prototype['rows'][0]['id']

        method = 'create'
        run_args = {'model': 'task',
                    'name': name,
                    'status': 'waiting',
                    'task_prototype_id': task_prototype_id,
                    'specification': specification}

        return self._request(method, run_args)

    def drop(self, model, names=None, ids=None):
        '''Drop database entries by name. Either names or ids must be
        specified.

        :param model: Model from which to drop entries.
        :type model: str
        :param names: A list of entry names (unique identifiers) to drop.
        :type names: list
        :param ids: A list of IDs in to drop.
        :type ids: list

        '''
        run_args = {'model': model}

        if not any([names, ids]):
            raise Exception('Must supply a names and/or ids agument.')

        if names is not None:
            run_args['names'] = names

        if ids is not None:
            run_args['ids'] = ids

        method = 'drop'
        return self._request(method, run_args)

    def modify(self, query_params):
        '''Not yet implemented.'''
        # TODO: Write once this is documented
        raise NotImplementedError('The "modify" method has no API docs.')

    def _request(self, method, args):
        '''Reusable method for making requests to the API'''
        data = {}
        data['login'] = self.login
        data['key'] = self.key
        run = {'method': method, 'args': args}
        data['run'] = run

        r = requests.post(self.url, json=data)
        # TODO: validate request error code
        if r.status_code != 200:
            print 'Returned status code: %{}'.format(r.status_code)
        else:
            json = r.json()
            # TODO: validate result ('status': OK)
            # TODO: provide a useful response message?
            return json
