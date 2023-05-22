import json

# transformed_json
output_json_object = {}

filepath = "./inputs/sample_input.json"


def print_json_object(json_object):
  json_formatted_str = json.dumps(json_object, indent=2)
  print(json_formatted_str)


# Read input json
def read_input(filepath):
  with open(filepath, 'r') as f:
    data = json.load(f)
    return data


def cast_to_string(s):
  valid = True
  s = s.strip()
  
  if s == "":
    valid = False
  
  return (valid, s)


def cast_to_number(s):
  return float(s.strip())


def cast_to_bool(s):
  true_values = ["1", "t", "T", "TRUE", "true", "True"]
  false_values = ["0", "f", "F", "FALSE", "false", "False"]

  s = s.strip()

  if s in true_values:
    return True
  elif s in false_values:
    return False


# Main
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
    casted_output_value = cast_to_number(output_value)
  elif data_type == "BOOL":
    casted_output_value = cast_to_bool(output_value)
  elif data_type == "S":
    valid, casted_output_value = cast_to_string(output_value)
      

  if valid:
    output_json_object[key] = casted_output_value

# Print output
print_json_object(output_json_object)
