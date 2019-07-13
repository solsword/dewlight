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
"""

import csv
import json
import os
import sys

if len(sys.argv) < 2:
  print("Usage: build_graph.py INPUT.tsv [OUTPUT.json] [REPLACE.json]")
  print("  You must supply at least the input file name.")

INPUT_FILE = sys.argv[1]
if len(sys.argv) > 2:
  OUTPUT_FILE = sys.argv[2]
elif INPUT_FILE.endswith(".tsv"):
  OUTPUT_FILE = INPUT_FILE[:-len(".tsv")] + "-graph.json"
else:
  OUTPUT_FILE = INPUT_FILE + "-graph.json"

# Input character -> replace with
if len(sys.argv) > 3:
  try:
    with open(sys.argv[3], 'r') as fin:
      REPLACE = json.load(fin)
  except:
    print("Warning could not read replacement file.")
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

with open(INPUT_FILE, 'r') as fin:
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

group_by = "initiated"

most = by_involvement[-1][group_by]
min_thr = 10
#min_thr = avg_init

print(
  "Main nodes must have {} more than {:.0f} connections.".format(
    group_by,
    most/2
  )
)
print(
  "Major nodes must have {} more than {:.0f} connections.".format(
    group_by,
    most*(1/3)
  )
)
print(
  "Minor nodes must have {} more than {:.1f} connections.".format(
    group_by,
    min_thr
  )
)
print(
  "Marginal nodes must have {} more than {:.0f} connections.".format(
    group_by,
    0
  )
)
print("Nodes who never {} a connection are Passive.".format(group_by))
top_half = [node for node in by_involvement if node[group_by] > most/2]
top_thirds = [node for node in by_involvement if node[group_by] > most*(1/3)]
ten_plus = [node for node in by_involvement if node[group_by] >= min_thr]
none = [node for node in by_involvement if node[group_by] == 0]

for node in GRAPH["nodes"]:
  node["group"] = 1

for node in none:
  node["group"] = 0

for node in ten_plus:
  node["group"] = 2

for node in top_thirds:
  node["group"] = 3

for node in top_half:
  node["group"] = 4

GRAPH["groups"] = [
  "Passive",
  "Marginal",
  "Minor",
  "Major",
  "Main"
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
