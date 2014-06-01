def remove_trailing_spaces(input_str):
  skip = True
  output_str = ""
  for c in input_str:
    if c != ' ' and skip == True:
      skip = False
    if skip == False:
      output_str += c
  return output_str

def form_indent(size):
  indent = ""
  for n in range(0, size):
    indent += " "
  return indent