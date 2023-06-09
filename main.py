import re
import json
from datetime import datetime
from collections import OrderedDict

filepath = "./inputs/sample_input.json"

# filepath = "./inputs/custom_input.json"
# filepath = "./inputs/another_custom_input.json"


# ============================ JSON Handlers ==============================
def read_input(filepath):
  with open(filepath, 'r') as f:
    data = json.load(f)
    return data


def print_json_object(json_object):
  json_formatted_str = json.dumps(json_object, indent=2)
  print(json_formatted_str)


def get_datatype_and_value(data_object):
  data_type = list(data_object.keys())[0]
  value = data_object[data_type]
  data_type = data_type.strip()

  return data_type, value


# ============================ Time and Epoch ==============================
def has_rfc3339_format(string):
  pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
  match = re.search(pattern, string)

  return True if match else False


def rfc3339_to_epoch(rfc3339_string):
  timestamp_format = "%Y-%m-%dT%H:%M:%SZ"
  dt = datetime.strptime(rfc3339_string, timestamp_format)
  return int(dt.timestamp())


# ============================ Transformations ==============================
def process_string(s):
  valid = True

  if s == "":
    valid = False
  elif has_rfc3339_format(s):
    s = rfc3339_to_epoch(s)

  return (valid, s)


def process_number(s):
  if s == "":
    return (False, None)

  num = 0
  try:
    num = int(s)
    return (True, num)
  except ValueError:
    num = 0

  try:
    num = float(s)
    return (True, num)
  except ValueError:
    num = 0

  return (False, None)


true_values = ["1", "t", "T", "TRUE", "true", "True"]
false_values = ["0", "f", "F", "FALSE", "false", "False"]


def process_bool(s):

  s = s.strip()

  if s in true_values:
    return (True, True)
  elif s in false_values:
    return (True, False)
  else:
    return (False, None)


def process_null(s):
  if s in true_values:
    return (True, None)
  else:
    return (False, None)


# DRY principle: This function is utilized in multiple places
# Process String, Number, Bool
def process_snb(data_type, output_value):
  output_value = output_value.strip()

  if data_type == "N":
    return process_number(output_value)
  elif data_type == "BOOL":
    return process_bool(output_value)
  elif data_type == "S":
    return process_string(output_value)

  return (False, None)


def process_list(l):
  if not isinstance(l, list):
    return (False, None)

  output_data_list = []

  for data_object in l:
    if isinstance(data_object, dict):
      data_type, value = get_datatype_and_value(data_object)
      valid, casted_output_value = process_snb(data_type, value)

      if valid:
        output_data_list.append(casted_output_value)

  if len(output_data_list) == 0:
    return (False, None)

  return (True, output_data_list)


def sort_map(output_json_object, output_keys):

  sorted_output_json_object = OrderedDict()

  sorted_output_keys = sorted(output_keys)
  for key in sorted_output_keys:
    sorted_output_json_object[key] = output_json_object[key]

  return sorted_output_json_object


def transform_json_object(input_json_object):

  output_json_object = {}

  for key, data_object in input_json_object.items():

    key = key.strip()
    if key == "":
      continue

    data_type, value = get_datatype_and_value(data_object)

    valid = True

    if data_type in ["N", "BOOL", "S"]:
      valid, casted_output_value = process_snb(data_type, value)
    elif data_type == "NULL":
      valid, casted_output_value = process_null(value.strip())
    elif data_type == "L":
      valid, casted_output_value = process_list(value)
    elif data_type == "M":
      valid, casted_output_value = transform_json_object(value)

    if valid:
      output_json_object[key] = casted_output_value

  output_keys = list(output_json_object.keys())

  if len(output_keys) == 0:
    return (False, None)

  sorted_output_json_object = sort_map(output_json_object, output_keys)

  return True, sorted_output_json_object


# ============================ Main ==============================

# read input json object
input_json_object = read_input(filepath)

# transform json object
valid, transformed_json_object = transform_json_object(input_json_object)

transformed_json_object = [transformed_json_object]  # to match output

# print transformed json object
print_json_object(transformed_json_object)
