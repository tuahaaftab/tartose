import re
import json
from datetime import datetime

# filepath = "./inputs/sample_input.json"
filepath = "./inputs/custom_input.json"


def has_rfc3339_format(string):
  pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
  match = re.search(pattern, string)

  if match:
    return True
  return False


def rfc3339_to_epoch(rfc3339_string):
  timestamp_format = "%Y-%m-%dT%H:%M:%SZ"
  dt = datetime.strptime(rfc3339_string, timestamp_format)
  return int(dt.timestamp())


def print_json_object(json_object):
  json_formatted_str = json.dumps(json_object, indent=2)
  print(json_formatted_str)


# Read input json
def read_input(filepath):
  with open(filepath, 'r') as f:
    data = json.load(f)
    return data


# Process String
def process_string(s):
  valid = True

  if s == "":
    valid = False
  elif has_rfc3339_format(s):
    s = rfc3339_to_epoch(s)

  return (valid, s)


# Process Number
def process_number(s):
  if s == "":
    return (False, s)

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

  return (False, num)


true_values = ["1", "t", "T", "TRUE", "true", "True"]
false_values = ["0", "f", "F", "FALSE", "false", "False"]


# Process Boolean
def process_bool(s):

  s = s.strip()

  if s in true_values:
    return (True, True)
  elif s in false_values:
    return (True, False)
  else:
    return (False, None)


# Process Null
def process_null(s):
  if s in true_values:
    return (True, None)
  else:
    return (False, s)


def get_datatype_and_value(data_object):
  data_type = list(data_object.keys())[0]
  value = data_object[data_type]

  return data_type, value


# Process List
def process_list(l):
  # Empty List | "L": "noop" | Expecting square brackets "L": ["noop"]
  if not isinstance(l, list):
    return (False, l)

  output_data_list = []

  for data_object in l:
    if isinstance(data_object, dict):
      data_type, value = get_datatype_and_value(data_object)
      valid, casted_output_value = process_nbs(data_type, value)

      if valid:
        output_data_list.append(casted_output_value)

  if len(output_data_list) == 0:
    return (False, None)
    
  return (True, output_data_list)


def process_nbs(data_type, output_value):
  output_value = output_value.strip()

  if data_type == "N":
    return process_number(output_value)
  elif data_type == "BOOL":
    return process_bool(output_value)
  elif data_type == "S":
    return process_string(output_value)

  return (False, None)


def transform_json_object(input_json_object):

  output_json_object = {}

  for key, data_object in input_json_object.items():

    key = key.strip()
    if key == "":
      continue

    data_type, value = get_datatype_and_value(data_object)

    valid = True

    # Based on value_type, cast to appropriate value
    # if data_type == "N":
    #   valid, casted_output_value = process_number(output_value.strip())
    # elif data_type == "BOOL":
    #   valid, casted_output_value = process_bool(output_value.strip())
    # elif data_type == "S":
    #   valid, casted_output_value = process_string(output_value.strip())

    if data_type in ["N", "BOOL", "S"]:
      valid, casted_output_value = process_nbs(data_type, value)
    elif data_type == "NULL":
      valid, casted_output_value = process_null(value.strip())
    elif data_type == "L":
      valid, casted_output_value = process_list(value)

    if valid:
      output_json_object[key] = casted_output_value

  return output_json_object


# ======= Main =========

input_json_object = read_input(filepath)
# print_json_object(input_json_object)

# transformed json object
transformed_json_object = transform_json_object(input_json_object)

# Print output
print_json_object(transformed_json_object)
