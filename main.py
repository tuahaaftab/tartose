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


# Process List
def process_list(l):
  # Empty List | "L": "noop" | Expecting square brackets "L": ["noop"]
  if not isinstance(l, list):
    return (False, l)

  # for elem in l:
  #   if isinstance(elem, dict):
  #     print(elem)

  return (True, l)


# Main

# transformed json object
output_json_object = {}

input_json_object = read_input(filepath)
# print_json_object(input_json_object)

for key, data in input_json_object.items():
  # print(key, value)

  key = key.strip()
  if key == "":
    continue

  data_type = list(data.keys())[0]
  output_value = data[data_type]

  valid = True

  # Based on value_type, cast to appropriate value
  if data_type == "N":
    valid, casted_output_value = process_number(output_value.strip())
  elif data_type == "BOOL":
    valid, casted_output_value = process_bool(output_value.strip())
  elif data_type == "S":
    valid, casted_output_value = process_string(output_value.strip())
  elif data_type == "NULL":
    valid, casted_output_value = process_null(output_value.strip())
  elif data_type == "L":
    valid, casted_output_value = process_list(output_value)

  if valid:
    output_json_object[key] = casted_output_value

# Print output
print_json_object(output_json_object)
