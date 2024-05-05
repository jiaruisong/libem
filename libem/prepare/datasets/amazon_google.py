import os
import json

import libem.prepare.datasets as datasets

path = os.path.join(datasets.LIBEM_SAMPLE_DATA_PATH, "amazon-google")
test_file = os.path.join(path, "test.ndjson")
train_file = os.path.join(path, "train.ndjson")
valid_file = os.path.join(path, "valid.ndjson")


def read_test(schema=True):
    # sample data:
    # {"id_left":"amazon_1191","title_left":"sims 2 glamour life stuff pack","manufacturer_left":"aspyr media","price_left":24.99,"cluster_id_left":810,
    #  "id_right":"google_567","title_right":"aspyr media inc sims 2 glamour life stuff pack","manufacturer_right":null,"price_right":23.44,"cluster_id_right":810,
    #  "label":1,"pair_id":"amazon_1191#google_567"}
    with open(test_file) as f:
        for line in f:
            data = json.loads(line.strip())
            parsed_data = {'left': {}, 'right': {}, 'label': data.get('label', None)}

            # clean the data
            trim = ["cluster_id_left", "cluster_id_right", "id_left", "id_right"]
            if schema:
                for key, value in data.items():
                    if key in trim:
                        continue
                    if key.endswith('_left'):
                        new_key = key[:-5]  # Remove '_left'
                        parsed_data['left'][new_key] = value
                    elif key.endswith('_right'):
                        new_key = key[:-6]  # Remove '_right'
                        parsed_data['right'][new_key] = value
            else:
                left_values, right_values = [], []
                for key, value in data.items():
                    if key in trim:
                        continue
                    # Skip null values
                    if value is None:
                        continue
                    if key.endswith('_left'):
                        left_values.append(str(value))
                    elif key.endswith('_right'):
                        right_values.append(str(value))
                parsed_data['left'] = ' '.join(left_values)
                parsed_data['right'] = ' '.join(right_values)

            yield parsed_data


def read_train():
    raise NotImplementedError


def read_valid():
    raise NotImplementedError


if __name__ == "__main__":
    import pprint

    pp = pprint.PrettyPrinter(sort_dicts=False)
    pp.pprint(next(read_test()))
    pp.pprint(next(read_test(schema=False)))