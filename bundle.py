#!/usr/bin/env python3
"""
bundle.py
Bundles data file into html file to create bundle.html.
"""

import sys

HTML = "index.html"
HELP = "help.html"
DATA = "data.json"
D3 = "d3/d3.v4.min.js"
OUT = "bundle.html"

if "-h" in sys.argv or "--help" in sys.argv:
  print("Usage: bundle.py [GRAPH.json] [BASE.html] [OUTPUT.html]")
  print("  Defaults are: graph.json, index.html, bundle.html")
  exit(1)

if len(sys.argv) > 1:
  DATA = sys.argv[1]
if len(sys.argv) > 2:
  HTML = sys.argv[2]
if len(sys.argv) > 3:
  HELP = sys.argv[3]
if len(sys.argv) > 4:
  OUT = sys.argv[4]

with open(HTML, 'r') as fin:
  src = fin.read()

with open(HELP, 'r') as fin:
  help = fin.read()

with open(DATA, 'r') as fin:
  data = fin.read()

with open(D3, 'r') as fin:
  d3 = fin.read()

def escape_html(help):
  # TODO: Worry about escaped double quotes in help string?
  return help.replace('"', '\\"').replace('\n', ' ')

help_assignment = 'inline_help = "{}"'.format(escape_html(help))
assignment = 'inline_data = {}'.format(data)
d3script = "<script type='text/javascript'>\n{}\n</script>".format(d3)

result = ''
for line in src.split('\n'):
  if line == 'inline_help = undefined;':
    result += help_assignment + '\n'
  elif line == 'inline_data = undefined;':
    result += assignment + '\n'
  elif line == '    <script src="d3/d3.v4.min.js"></script>':
    result += d3script + '\n'
  else:
    result += line + '\n'


with open(OUT, 'w') as fout:
  fout.write(result)
