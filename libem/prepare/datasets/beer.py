import os
import json

import libem.prepare.datasets as datasets

description = "This dataset contains beer data from BeerAdvocate and RateBeer. " \
              "It was created by students in the CS 784 data science class at UW-Madison, " \
              "Fall 2015, as a part of their class project."

# sample data:
# {"beer_name_left": "Bulleit Bourbon Barrel Aged G'Knight", "brew_factory_name_left": "Oskar Blues Grill & Brew", "style_left": "American Amber / Red Ale", "abv_left": "8.70 %",
# "beer_name_right": "Figure Eight Bourbon Barrel Aged Jumbo Love", "brew_factory_name_right": "Figure Eight Brewing", "style_right": "Barley Wine", "abv_right": "",
# "label": 0}
def read(file, schema=True, **kwargs):
    with open(file) as f:
        for line in f:
            data = json.loads(line.strip())
            
            keep_null = 'keep_null' in kwargs and kwargs['keep_null']
            fields = kwargs['fields'] if 'fields' in kwargs else []
            parsed_data = {'left': None, 'right': None, 'label': data.get('label', None)}
            left_values, right_values = {}, {}

            # clean the data
            if schema:
                for key, value in data.items():
                    # Change null values to empty str
                    if not keep_null and value is None:
                        value = ''
                    if key.endswith('_left'):
                        new_key = key[:-5]  # Remove '_left'
                        if len(fields) == 0 or new_key in fields:
                            left_values[new_key] = value
                    elif key.endswith('_right'):
                        new_key = key[:-6]  # Remove '_right'
                        if len(fields) == 0 or new_key in fields:
                            right_values[new_key] = value
                
                # order output fields
                if len(fields) > 0:
                    parsed_data['left'] = {field: left_values[field] for field in fields}
                    parsed_data['right'] = {field: right_values[field] for field in fields}
                else:
                    parsed_data['left'] = left_values
                    parsed_data['right'] = right_values
                        
            else:
                for key, value in data.items():
                    if key in kwargs and kwargs[key] == False:
                        continue
                    # Change null values to empty str
                    if not keep_null and value is None:
                        value = ''
                    if key.endswith('_left'):
                        new_key = key[:-5]  # Remove '_left'
                        if len(fields) == 0 or new_key in fields:
                            left_values[new_key] = str(value)
                    elif key.endswith('_right'):
                        new_key = key[:-6]  # Remove '_right'
                        if len(fields) == 0 or new_key in fields:
                            right_values[new_key] = str(value)
                
                if len(fields) > 0:
                    parsed_data['left'] = ' '.join([left_values[field] for field in fields])
                    parsed_data['right'] = ' '.join([right_values[field] for field in fields])
                else:
                    parsed_data['left'] = ' '.join(left_values.values())
                    parsed_data['right'] = ' '.join(right_values.values())

            yield parsed_data


def read_test(schema=True, **kwargs):
    '''
    Yields processed records from the dataset one at a time.
    args:
        schema (bool): whether to include the schema or not
    kwargs:
        version (int): the version of the dataset to use, default to 0.
        keep_null (bool): if False, replace null values with empty str, else keep as 'None'.
        fields (list[str]): fields (and their order) to include in the output, 
                            empty to include all fields. Do not include _left/_right.
    '''
    version = int(kwargs['version']) if 'version' in kwargs else 0
    path = os.path.join(datasets.LIBEM_SAMPLE_DATA_PATH, "beer")
    test_file = os.path.join(os.path.join(path, f'v{version}'), 'test.ndjson')
    
    return read(test_file, schema, **kwargs)


def read_train(schema=True, **kwargs):
    '''
    Yields processed records from the dataset one at a time.
    args:
        schema (bool): whether to include the schema or not.
    kwargs:
        version (int): the version of the dataset to use, default to 0.
        keep_null (bool): if False, replace null values with empty str, else keep as 'None'.
        fields (list[str]): fields (and their order) to include in the output, 
                            empty to include all fields. Do not include _left/_right.
    '''
    version = int(kwargs['version']) if 'version' in kwargs else 0
    path = os.path.join(datasets.LIBEM_SAMPLE_DATA_PATH, "beer")
    train_file = os.path.join(os.path.join(path, f'v{version}'), 'train.ndjson')
    
    return read(train_file, schema, **kwargs)


def read_valid():
    raise NotImplementedError


if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter(sort_dicts=False)
    pp.pprint(next(read_test()))
    pp.pprint(next(read_test(schema=False)))
