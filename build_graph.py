#!/usr/bin/env python3
"""
build_graph.py

Data processing to produce a .json graph file from a .tsv tab-separated values
file. The TSV file must have a header line naming all of the columns, and must
at least have the following columns:

  'initiator'
  'recipient'

When commas are present, values will be presumed to indicate multiple
participating nodes, and individual links from each initiator to each recipient
will be added to the graph.

TODO: Document replace + groups file formats + behavior
"""

import csv
import json
import os
import sys

USAGE = """\
Usage:
  build_graph.py INPUT.tsv [-g GROUPS.json] [-r REPLACE.json] [-o OUTPUT.json]\
"""

if len(sys.argv) < 2:
  print(USAGE)
  print("  You must supply at least the input file name.")
  exit(1)

INPUT_FILE = sys.argv[1]
extra_args = sys.argv[2:]

if len(extra_args) % 2 != 0:
  print(USAGE)
  print("  You must supply an even number of extra arguments.")
  exit(1)

GROUPS_FILE = None
REPLACE_FILE = None
OUTPUT_FILE = None

while extra_args:
  flag = extra_args[0]
  filename = extra_args[1]
  extra_args = extra_args[2:]

  if flag == "-g":
    GROUPS_FILE = filename
  elif flag == "-r":
    REPLACE_FILE = filename
  elif flag == "-o":
    OUTPUT_FILENAME = filename
  else:
    print(USAGE)
    print("  You may only use flags -g, -r, and/or -o.")
    exit(1)

# Look for default files by name if they weren't provided:
if GROUPS_FILE == None:
  groups_test = os.path.splitext(INPUT_FILE)[0] + "-groups.json"
  if os.path.exists(groups_test):
    GROUPS_FILE = groups_test

if REPLACE_FILE == None:
  replace_test = os.path.splitext(INPUT_FILE)[0] + "-replace.json"
  if os.path.exists(replace_test):
    REPLACE_FILE = replace_test

if OUTPUT_FILE == None:
  OUTPUT_FILE = os.path.splitext(INPUT_FILE)[0] + "-graph.json"

# Input character -> replace with
if REPLACE_FILE != None:
  try:
    with open(REPLACE_FILE, 'r') as fin:
      REPLACE = json.load(fin)
  except:
    print("Warning: could not read replacement file.")
    REPLACE = {}
else:
  REPLACE = {}

DIALECT = "excel-tab"

GRAPH = {
  "nodes": [],
  "groups": [],
  "links": [],
  "dlinks": [],
}

node_ids = {}
link_ids = {}
dlink_ids = {}

soliloquists = set()
all_characters = set()

with open(INPUT_FILE, 'r', newline='') as fin:
  reader = csv.DictReader(fin, dialect=DIALECT)

  # First accumulate records by splitting multi-recipient/multi-initiator rows:
  records = []
  for row in reader:
    #if ',' in initiator or ',' in recipient:
    #  print("Compound: {} -> {}".format(initiator, recipient))

    # Initiators
    initiator = row["initiator"]
    initiators = [i.strip() for i in initiator.split(',')]
    initiators = [REPLACE.get(x, x) for x in initiators]
    all_characters.update(initiators)

    # Recipients
    recipient = row["recipient"]
    recipients = [r.strip() for r in recipient.split(',')]
    recipients = [REPLACE.get(x, x) for x in recipients]
    all_characters.update(recipients)

    # Subjects
    if "subject" in row:
      subject = row["subject"]
      subjects = [x.strip() for x in subject.split(',')]
      subjects = [REPLACE.get(x, x) for x in subjects]
      all_characters.update(subjects)

    # Present
    if "present" in row:
      present = row["present"]
      present = [x.strip() for x in present.split(',')]
      present = [REPLACE.get(x, x) for x in present]
      all_characters.update(present)

    for i in initiators:
      for r in recipients:
        records.append([i, r])

  # Next iterate through individualized interactions to create our graph:
  for initiator, recipient in records:
    if initiator == recipient:
      soliloquists.add(initiator) # self-links are processed

    if initiator not in node_ids:
      new_node = {
        "id": initiator,
        "group": 0,
        "involved": 1,
        "initiated": 1,
        "received": 0,
      }
      node_ids[initiator] = new_node
      GRAPH["nodes"].append(new_node)
    else:
      node = node_ids[initiator]
      node["involved"] += 1
      node["initiated"] += 1

    if recipient not in node_ids:
      new_node = {
        "id": recipient,
        "group": 0,
        "involved": 1,
        "initiated": 0,
        "received": 1,
      }
      node_ids[recipient] = new_node
      GRAPH["nodes"].append(new_node)
    else:
      node = node_ids[recipient]
      node["involved"] += 1
      node["received"] += 1

    lid = "{}---{}".format(*sorted([initiator, recipient]))
    if lid not in link_ids:
      new_link = {
        "source": initiator,
        "target": recipient,
        "value": 1
      }
      link_ids[lid] = new_link
      GRAPH["links"].append(new_link)
    else:
      link = link_ids[lid]
      link["value"] += 1

    dlid = "{}---{}".format(initiator, recipient)
    if dlid not in dlink_ids:
      new_dlink = {
        "source": initiator,
        "target": recipient,
        "value": 1
      }
      dlink_ids[dlid] = new_dlink
      GRAPH["dlinks"].append(new_dlink)
    else:
      dlink = dlink_ids[dlid]
      dlink["value"] += 1

by_involvement = sorted(
  GRAPH["nodes"],
  key=lambda node: (
    node["initiated"],
    node["received"],
    node["id"]
  )
)

avg_init = sum(x["initiated"] for x in by_involvement)/len(by_involvement)

# Groups
if GROUPS_FILE != None:
  # Determine groups from file contents:
  group_data = None
  try:
    with open(GROUPS_FILE, 'r') as fin:
      group_data = json.load(fin)
  except:
    print("Warning: could not read groups file.")
    raise

  if group_data == None:
    for node in GRAPH["nodes"]:
      node["group"] = "None"

    GRAPH["groups"] = [ { "id": "None", "tags": [] } ]
  else:
    for id in group_data["assignments"]:
      group = group_data["assignments"][id]
      for node in GRAPH["nodes"]:
        if node["id"] == id:
          node["group"] = group
    GRAPH["groups"] = []
    for group_id in group_data["tags"]:
      GRAPH["groups"].append(
        { "id": group_id, "tags": group_data["tags"][group_id] }
      )
else:
  # Determine groups from node stats:
  group_by = "initiated"

  most = by_involvement[-1][group_by]
  main_thr = most/2
  major_thr = most/3
  minor_thr = avg_init
  if minor_thr >= major_thr/2:
    minor_thr = major_thr/2

  print(
    "Main nodes must have {} more than {:.1f} connections.".format(
      group_by,
      most/2
    )
  )
  print(
    "Major nodes must have {} more than {:.1f} connections.".format(
      group_by,
      most*(1/3)
    )
  )
  print(
    "Minor nodes must have {} more than {:.1f} connections.".format(
      group_by,
      minor_thr
    )
  )
  print(
    "Marginal nodes must have {} more than {:.1f} connections.".format(
      group_by,
      0
    )
  )
  print("Nodes who never {} a connection are Passive.".format(group_by))
  main = [node for node in by_involvement if node[group_by] > main_thr]
  major = [node for node in by_involvement if node[group_by] > major_thr]
  minor = [node for node in by_involvement if node[group_by] > minor_thr]
  passive = [node for node in by_involvement if node[group_by] == 0]

  for node in GRAPH["nodes"]:
    node["group"] = "Marginal"

  for node in passive:
    node["group"] = "Passive"

  for node in minor:
    node["group"] = "Minor"

  for node in major:
    node["group"] = "Major"

  for node in main:
    node["group"] = "Main"

  GRAPH["groups"] = [
    { "id": "Passive", "tags": ["fringe"] },
    { "id": "Marginal", "tags": ["outside"] },
    { "id": "Minor", "tags": [ "core" ] },
    { "id": "Major", "tags": [ "core" ] },
    { "id": "Main", "tags": [ "core" ] },
  ]

initiators = [node for node in GRAPH["nodes"] if node["initiated"] > 0]
recipients = [node for node in GRAPH["nodes"] if node["received"] > 0]

pure_soliloquists = [
  sol
    for sol in soliloquists
    if not any(node["id"] == sol for node in GRAPH["nodes"])
]

print("# of initiating nodes: {}".format(len(initiators)))
print("# of receiving nodes: {}".format(len(recipients)))
print("# of nodes who connected with themselves: {}".format(len(soliloquists)))
print(
  "# of nodes who connected only with themselves: {}".format(
    len(pure_soliloquists)
  )
)
print("Total # of nodes in graph: {}".format(len(GRAPH["nodes"])))
print("Total # of nodes mentioned: {}".format(len(all_characters)))

with open(OUTPUT_FILE, 'w', encoding="utf-8") as fout:
  json.dump(GRAPH, fout, ensure_ascii=False)

if not os.path.isdir("lists"):
  if os.path.exists("lists"):
    print("Error: 'lists' exists but is not a directory!")
    exit(1)
  os.mkdir("lists")

with open(
  os.path.join("lists", "all_nodes.txt"),
  'w',
  encoding="utf-8"
) as fout:
  for name in sorted(all_characters):
    fout.write(name + '\n')

with open(
  os.path.join("lists", "active_nodes.txt"),
  'w',
  encoding="utf-8"
) as fout:
  for node in sorted(GRAPH["nodes"], key=lambda x: x["id"]):
    fout.write(node["id"] + '\n')

with open(
  os.path.join("lists", "initiators.txt"),
  'w',
  encoding="utf-8"
) as fout:
  for node in sorted(initiators, key=lambda x: x["id"]):
    fout.write(node["id"] + '\n')

with open(
  os.path.join("lists", "recipients.txt"),
  'w',
  encoding="utf-8"
) as fout:
  for node in sorted(recipients, key=lambda x: x["id"]):
    fout.write(node["id"] + '\n')

with open(
  os.path.join("lists", "soliloquists.txt"),
  'w',
  encoding="utf-8"
) as fout:
  for name in sorted(soliloquists):
    fout.write(name + '\n')
