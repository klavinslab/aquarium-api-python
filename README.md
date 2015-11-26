# aquarium-api-python
Python library for interacting with the aquarium web API

# Installation

`cd directory/that/contains/setup.py`
`pip install .`

# Usage

## Importing

    from aquariumapi import AquariumAPI

## Initializing the API object

The AquariumAPI object provides methods for making requests to the API. It
stores the location of the API and your credentials so that they only need to
be entered once at the beginning of your script:

    api = AquariumAPI("http://bioturk.ee.washington.edu:3011/api", "bolten", "nt4kljdjFJFDSK4233lkjfADNF")`

The first argument is the URL of the api - this comes in the format of `"{base aquarium URL}/api"`. Make sure to use the testing server to validate your submissions if you're creating new samples/items/tasks!

The second argument is your aquarium username.

The third argument is your aquarium API key, which can be found by clicking Account&gt;Profile and generating a key

## Making requests

There are two options for interacting with the API once the AquariumAPI object
has been initialized:

1. Use the AquariumAPI object directly to make requests that are a thin wrapper
around the actual JSON being submitted (the methods available mirror those of
the API (https://github.com/klavinslab/aquarium/blob/master/doc/API.md).

2. Use the two model helper classes, `models.SampleModel` and
`models.TaskModel`.

These two approaches are discussed below.

### Using AquariumAPI directly to make requests

#### find

##### arguments:
`model`:  defines the database model you want to query - for example, "sample" or "item".
`where`: An optional argument. If not supplied, returns all the rows for the model. If supplied, should be a dictionary that defines the exact query you want to run (see the API documentation to view the syntax required).

#### create

##### arguments:
`model`:  Database model in which the new entry will be created - e.g. "sample".
`model_type`: Type within the model to be generated - e.g. if the `model` is "sample" a `model_type` could be "Primer".
`name`:  Name of the new entry.
`description`:  Description of the new entry.
`fields`:  A dictionary of fields of the new entry - specific to each type within the model. [Click here](http://bioturk.ee.washington.edu:3011/sample_types) for a list of fields required for sample types.

#### drop_by_names

##### arguments:
`model`:  Database model in which the new entry will be deleted - e.g. "sample".
`names`:  A list of names for the entries you want to delete
`ids`:  A list of IDs for the entries you want to delete

### Using the models module to make requests

The `models` module makes it more convenient to find and interact with samples
and tasks. The module is agnostic to the exact samples or tasks available in a
given instance of Aquarium and can be used to discover them. For example, a
plant lab may have a sample of type 'Arabidopsis' while a biophysics lab may
have a sample of type 'RNA'.

If you already know the exact name of the Sample type (e.g. Plasmid) or Task
type (e.g. Gibson Assembly), you can initialize them directly (note that they
require an AquariumAPI instance as the first argument):

    plasmid_model = aquariumapi.models.SampleModel(api, 'Plasmid')
    plasmid_model.find({'name': 'my_plasmid_name'})
    plasmid_model.info()
    plasmid_model.create({'Sequence': 'http://benchling.com/whatevs'}, 'myproject)

    gibson_tasks = aquariumapi.models.TaskModel(api, 'Gibson Assembly')
    gibson_tasks.info()
    plasmid_model.create({'item_ids': [3,5,6]})

Note the use of the `.info()` method. This displays the arguments available for
creating a new sample or task. The methods available to a given SampleModel
or TaskModel mirror those of the AquariumAPI object, but you do not need to
enter the 'model' argument anymore and other sane defaults are set for you
automatically.

If you don't already know the exact name of the Sample type or Task type, you
can automatically generate all of the SampleModels and TaskModels that can be
defined for your server:

    sample_models = aquariuapi.models.get_sample_definitions()
    print plasmid_model
    plasmid_model = sample_models['Plasmid']
    task_models = aquariumapi.models.get_task_definitions()

The object returned by the `get_x_definitions` functions is just a dictionary
with keys being the model type names (e.g. 'Plasmid'). The values are
instances of the appropriate model class, e.g. an instantiated SampleModel
that can be used immediately to find, create, and drop rows.
