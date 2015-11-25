'''Classes for interacting with the API models of Aquarium servers.'''
import json


class SampleModel(object):
    '''Accesses samples via the API.'''
    def __init__(self, api, sample_type):
        '''
        :param api: An instance of the Aquarium API client.
        :type api: aquariumapi.AquariumAPI
        :param sample_type: The exact name for the sample type definition. This
                            is used to look up the info (including fields) for
                            this sample type.
        :type sample_type: str
        :param fields: A list of lists of field-type pairs (used solely as
                       information for the user) for the sample type, e.g.
                       for a Primer it may be [['Overhang', 'string'],
                       ['Anneal', 'string']].
        :type fields: list
        :param id_: The id of the sample type (used solely as information for
                    the user).
        :type id_: int

        '''
        self.api = api
        self.sample_type = sample_type
        sample_type_info = api.find('sample_type',
                                    {'name': self.sample_type})['rows'][0]

        self.id = sample_type_info['id']
        self.fields = []
        # Hard-coded field number is 8
        for i in range(1, 8):
            if sample_type_info['field{}type'.format(i)] != 'not used':
                field_name = str(sample_type_info['field{}name'.format(i)])
                field_type = str(sample_type_info['field{}type'.format(i)])
                self.fields.append([field_name, field_type])

    def info(self):
        '''Displays sample type, id, and field information.'''
        return {'sample_type': self.sample_type, 'id': self.id,
                'fields': self.fields}

    def find(self, where=None, limit=None):
        '''Finds samples of this type using the same syntax as the built-in
        AquariumAPI methods.

        :param where: Query for selecting subsets of this sample type. Input
                      type is identical to that for AquariumAPI.find
        :type where: dict
        :param limit: Limits the number of returned rows to this number.
        :type limit:

        '''
        if where is None:
            where = {}

        # If self.id is set, add it to the 'where' query.
        if self.id is not None:
            where['sample_type_id'] = self.id

        return self.api.find('sample', where=where, limit=limit)

    def create(self, name, description, fields, project):
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
    def __init__(self, api, task_type):
        self.api = api
        self.task_type = task_type

        task_prototype = api.find('task_prototype',
                                  {'name': task_type})['rows'][0]
        self.id = task_prototype['id']
        # Get prototype
        # FIXME: why isn't it already JSON?
        self.prototype = json.loads(task_prototype['prototype'])

    def info(self):
        '''Displays sample type, id, and field information.'''
        return {'task_type': self.task_type, 'id': self.id,
                'prototype': self.prototype}

    def find(self, where=None, limit=None):
        if where is None:
            where = {}

        # If self.id is set, add it to the 'where' query.
        if self.id is not None:
            where['task_prototype_id'] = self.id

        return self.api.find('task', where=where, limit=limit)

    def create(self, name, specification):
        return self.api.create_task(name, self.task_type, specification)

    def drop(self):
        raise NotImplementedError

    def modify(self, args):
        raise NotImplementedError

    def __repr__(self):
        return '{} TaskModel'.format(self.task_type)


def get_sample_definitions(api):
    sample_types = api.find('sample_type')['rows']

    models = {}
    for sample_type in sample_types:
        models[sample_type['name']] = SampleModel(api, sample_type['name'])

    return models


def get_task_definitions(api):
    task_prototypes = api.find('task_prototype')['rows']

    models = {}
    for task_prototype in task_prototypes:
        models[task_prototype['name']] = TaskModel(api, task_prototype['name'])

    return models
