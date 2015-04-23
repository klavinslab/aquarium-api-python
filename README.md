# aquarium-api-python
Python library for interacting with the aquarium web API

# Usage

There's no setup.py yet, so copy the aquarium directory (contains __init__.py)
into the current directory to use it.

### Importing

    from aquarium import AquariumAPI

### Initializing the API object

this temporarily stores the location of the
aquarium API url, your username, and your password so you only have to input
it once.

    api = AquariumAPI("http://bioturk.ee.washington.edu:3011/api", "bolten", "nt4kljdjFJFDSK4233lkjfADNF")`

The first argument is the URL of the api - this comes in the format of `"{base aquarium URL}/api"`. Make sure to use the testing server to validate your submissions if you're creating new samples/items/tasks!

The second argument is your aquarium username.

The third argument is your aquarium API key, which can be found by clicking Account&gt;Profile and generating a key

### Making requests

The methods available mirror those of the API (https://github.com/klavinslab/aquarium/blob/master/doc/API.md) and include:
* find
* create
* drop_by_names
* drop_by_ids

#### find

##### arguments:
`model`:  defines the database model you want to query - for example, "sample" or "item".
`where_query`: defines the exact query you want to run (see the API documentation to view the syntax required).

#### create

##### arguments:
`model`:  Database model in which the new entry will be created - e.g. "sample".
`model_type`: Type within the model to be generated - e.g. if the `model` is "sample" a `model_type` could be "Primer".
`name`:  Name of the new entry.
`description`:  Description of the new entry.
`fields`:  Fields of the new entry - specific to each type within the model. [Click here](http://bioturk.ee.washington.edu:3011/sample_types) for a list of fields required for sample types.

#### drop_by_names

##### arguments:
`model`:  Database model in which the new entry will be deleted - e.g. "sample".
`names`:  A list of names for the entries you want to delete

#### drop_by_ids

##### arguments:
`model`:  Database model in which the new entry will be deleted - e.g. "sample".
`ids`:  A list of IDs for the entries you want to delete
