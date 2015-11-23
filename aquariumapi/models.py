'''Classes for interacting with the API models of Aquarium servers.'''


class SampleModel(object):
    '''Accesses samples via the API.'''
    def __init__(self, api, sample_type, fields=None, id_=None, project=None):
        '''
        :param api: An instance of the Aquarium API client.
        :type api: aquariumapi.AquariumAPI
        :param sample_type: The exact 'name' for the sample type definition.
        :type sample_type: str
        :param fields: A list of lists of field-type pairs (used solely as
                       information for the user) for the sample type, e.g.
                       for a Primer it may be [['Overhang', 'string'],
                       ['Anneal', 'string']].
        :type fields: list
        :param id_: The id of the sample type (used solely as information for
                    the user).
        :type id_: int
        :param project: The project with which to associate any samples created
                        by this object. Can be set on a per-creation basis
                        as well.
        :type project: str

        '''
        self.api = api
        self.sample_type = sample_type
        self.project = project
        self.fields = fields
        self.id = id_

    def info(self):
        '''Displays sample type, id, and field information.'''
        return {'sample_type': self.sample_type, 'id': self.id,
                'fields': self.fields}

    def find(self, where_query=None, limit=None):
        '''Finds samples of this type using the same syntax as the built-in
        AquariumAPI methods.

        :param where_query: Query for selecting subsets of this sample type.
                            Input type is identical to that for
                            AquariumAPI.find
        :type where_query: dict
        :param limit: Limits the number of returned rows to this number.
        :type limit:

        '''
        return self.api.find('sample', where_query, limit)

    def create(self, name, description, fields, project=None):
        '''Creates a new row of this sample type in the database.

        :param name: Name of the sample.
        :type name: str
        :param description: Desription of the sample.
        :type description: str
        :param fields: Information fields to add to this sample. You can find
                       the fields and their types with the .info() method.
                       Add as field:value pairs in a dictionary.
        :type fields: dict
        :param project: The project with which to associate this sample.
        :type project: str

        '''
        if project is None:
            project = self.project

        return self.api.create_sample(self.sample_type, name, description,
                                      fields, project)

    def drop(self, names=None, ids=None):
        '''Drop entries using either a list of sample IDs or a list of names
        (only names or ids may be set).

        :param names: A list of names (strings) of the samples to drop.
        :type names: list
        :param ids: A list of IDs (ints) of the samples to drop.
        :type ids: list

        '''
        if not any([names, ids]) or all([names, ids]):
            raise Exception('Must supply either the names or ids agument.')

        if names is not None:
            self.api.drop_by_names('sample', names)

        if ids is not None:
            self.api.drop_by_ids('sample', ids)

    def modify(self, args):
        raise NotImplementedError

    def __repr__(self):
        return '{} SampleModel'.format(self.sample_type)


class TaskModel(object):
    def __init__(self, api, task_type, project=None):
        self.api = api
        self.task_type = task_type
        self.project = project

    def find(self, where_query=None, limit=None):
        return self.api.find('task', where_query, limit)

    def create(self, name, specification, project=None):
        if project is None:
            project = self.project

        return self.api.create_task(name, self.task_type, specification,
                                    project)

    def drop(self):
        raise NotImplementedError

    def modify(self, args):
        raise NotImplementedError


def get_sample_definitions(api, project=None):
    sample_types = api.find('sample_type')['rows']

    def get_sample_model(sample_type, project=None):
        # Create instances of SampleModel
        name = sample_type['name']
        id_ = sample_type['id']
        # Hard-coded field number is 8
        n_fields = 8
        fieldinfo = []
        for i in range(1, n_fields):
            if sample_type['field{}type'.format(i)] != 'not used':
                field_name = str(sample_type['field{}name'.format(i)])
                field_type = str(sample_type['field{}type'.format(i)])
                fieldinfo.append([field_name, field_type])

        # clsname = ''.join([word.capitalize() for word in name.split(' ')])

        cls = SampleModel(api, name, fields=fieldinfo, id_=id_,
                          project=project)

        return cls

    models = {}
    for sample_type in sample_types:
        models[sample_type['name']] = get_sample_model(sample_type,
                                                       project=project)

    return models
