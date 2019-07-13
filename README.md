# Dewlight

Network visualizer.

## Dependencies

- Python 3 for:
    * building graphs
    * bundling standalone HTML files
    * running a simple web server

- Running `chrome --allow-file-access-from-files` or a different browser with a
  similar ability to suspend CORS rules for files should allow you to open
  `index.html` and visualize the provided `example-graph.json` file (or a graph
  `.json` file of your choice, using `?t=...` at the end of your URL) without
  needing to run Python.

## Features:

- Build a network from a `.tsv` tab-separated-value file that lists initiated
  and received interactions.
- Automatically categorize nodes based on relative activity.
- Interactive node selection and labeling.
- Visualize a network in several ways:
    * Using a force-directed graph where low-interaction and non-initiating
      nodes are pushed to the edges.
    * As a histogram of initiated/received interaction counts.
    * As an ego network, showing direct connections from a selected node.
    * As an affinity plot, showing for several nodes their relative interaction
      levels with a group of framing nodes. (TODO)
- Ability to sort & filter/find nodes in a list.
- Random-search "optimization" of force-directed layouts.
    * TODO: evolutionary approach or at least local refinement.

## TODO
