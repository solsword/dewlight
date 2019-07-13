# Dewlight

Network visualizer.

Features:

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
