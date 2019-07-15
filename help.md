# Help

## About {#help:about}

Dewlight is a visualization tool for networks, specialized for medium-size
networks with perhaps dozens of nodes, where edges are directional and
weighted. It has multiple tools for visualizing connections between nodes and
their relationships to each other. The visualization tools include:

- [Relationships](#help:relationships): This view shows the relationships
  between all nodes, with thicker lines connecting nodes that have stronger
  relationships. It treats relationships as reciprocal, and adds up the
  strength of connections in both directions between two nodes. Nodes are laid
  out on a grid so that nodes with stronger connections are closer to each
  other, and then a force simulation is used to relax their positions.
- [Ego Network](#help:ego_network): This view shows all of the connections from
  and to a single node. It displays directed edges separately, and arranges
  connected nodes in a circle around the central node.
- [Affinity Plot](#help:affinity_plot): This view shows the relative strength
  of connections to a group of reference nodes. The reference nodes are placed
  on the perimeter of a circle, and nodes of interest are placed inside,
  located based on their relative connection strength to each outer node. Like
  the relationships graph the affinity plot treats connections as reciprocal.
- [Histograms](#help:histograms): This view provides a more abstract view of
  the network, showing a histogram of one of several properties, like the
  number of initiated connections from each node, or the number of neighbors
  each node has. It can also display two histograms simultaneously to compare
  them.

At the top left, the controls area shows [global controls](#help:controls) and
graph-specific controls (described in the help sections for each type of
graph). The global controls are:

- The "show" drop-down menu controls which view is displayed.
- The "filter nodes" check box controls whether all nodes are shown, or whether
  only important nodes are shown. It applies across all views, and also filters
  edges (only edges among included nodes are counted).
- The "clear selection" button allows you to deselect all currently selected
  nodes.
- The "mark" menu controls which nodes are marked with a symbol in the current
  view and the [listing](#help:listing). The symbols can help you see which
  node is which without hovering over it, but can also be distracting.

At the top right, there is a legend that shows the colors used for the current
view. For most views, color is based on group, which is discussed in the
[colors](#help:colors) section.

On the bottom left, the current view is displayed. In all views, you can click
on nodes (or bars in the [histograms](#help:histograms) view) to select them.
Selections filter which edges are visible, and also control how the [ego
network](#help:ego_network) and [affinity plot](#help:affinity_plot) views
behave.

On the bottom right, the [listing](#help:listing) displays the ID of each node,
along with its assigned symbol (if any), the number of neighbors it has, and
the number of initiated, received, and total connections for that node.

## Relationships {#help:relationships}

The relationships view displays the connections among all nodes in the graph,
using an automatic layout that tries to put more-connected nodes close to each
other, starting from the most-connected node. The positions in the graph can
thus be interpreted (with caution) as implying relationships among nodes (use
other views to confirm these).

You can drag around the nodes to adjust their position, but when you do that,
the rest of the nodes will be allowed to move according to their constraints.
By hovering over a node or selecting nodes (by clicking on them), you can limit
which edges are shown, and hovering on a node or edge for a moment will display
information about it.

The controls for this view are:

- The "hide" check boxes for "minor edges" and "passive edges." These allow you
  to hide all edges that connect to minor (or passive) nodes, to reduce
  clutter.
- The "layout" selector, which allows you to switch between the "strict,"
  "loose," and "relaxed" layouts (see below).
- The "reset layout" button, which puts nodes back to their original positions
  for the selected layout.
- The "relax further" button, which allows the nodes to settle more under the
  physical simulation rules (see below).

The position of the nodes is governed by two processes: the initial layout, and
a physical simulation that includes several simulated forces.

### Initial Layout

The initial layout results can be viewed without running the physical
simulation at all by selecting the "strict" layout option. This layout places
nodes on a triangular grid. To produce this layout, the following algorithm is
used:

1. At each step, select a single node to place on the graph:
    - For the first step, use the node that has the highest total combined
      interaction weight (weight of all outgoing + incomming links).
    - For subsequent steps, pick the node that has the most interaction weight
      with nodes that have already been placed. Ties are broken by total
      interaction weight across all nodes, then by number of neighbors, then by
      group (more-interacting groups first; see [colors](#help:colors)), and
      finally by ascending alphabetical order of node IDs.
2. Next, place that node on the graph:
    - For the first step, place it at the origin (0, 0).
    - For subsequent nodes, examine all empty grid locations that are adjacent
      to an already-placed node:
          * At each location, compute the cost for that location as the
            weighted sum of the link lengths of each link from this node to a
            node that's already been placed. This is just the length of each
            link (if the node were at this location) times its weight.
          * Pick the locaiton that has the lowest total cost, and put the node
            there. Ties are broken by choosing locations that are closer to the
            origin, and double-ties are broken by choosing the edge position
            that was added to the list of edge positions first.
3. Finally, repeat steps 1 and 2 until all nodes have been placed (including
   nodes not connected to the original node).

This algorithm normally results in a roughly hexagonal group of nodes, even
when connections aren't thick, because it breaks ties towards the origin. The
default listing sort order for this view shows the order in which nodes were
added, which can help understand the layout, but in general, and especially for
the first several characters placed, proximity in the layout indicates relative
strength of connection (as things get crowded the grid constraints make this
less strictly true).

Once the nodes are positioned in this grid, in the "loose" and "relaxed"
layouts, relax those positions by simulating a few physical forces acting on
the nodes in two dimensions.

### Physical Simulation

When the "relax" further button is clicked, when a node is dragged, or during
layout construction for the "loose" and "relaxed" layouts, physical forces are
simulated to position the nodes. The two main forces are:

- A repulsion force that pushes all nodes away from each other when they get
  too close. This prevents nodes from piling up and obscuring each other, but
  it also is the primary source of distortion that causes nodes *not* to be
  positioned as close to their neighbors as they would naturally be.
- An attraction force along each link, that as long as the nodes aren't
  overlapping, pulls them closer to each other, and gets stronger the farther
  the link is stretched. The strength of the attraction force is also
  proportional to the logarithm of the link value, so higher-weighted links
  pull a bit harder (but it's not a huge difference).

In addition to these two main forces, there are several more forces to help
arrange the nodes:

- A gathering force pulls all nodes towards the origin. This ensures that
  disconnected nodes to not drift away from the main part of the graph. This
  force is fairly weak, so it does not introduce very much distortion.
- A "bubble" force that forces nodes in certain categories out of the center
  of the graph. Nodes with less than 10 total link weight (incoming +
  outgoing) are considered "marginal," and they are all pushed outward from the
  center a set distance by a very strong force that's stronger than most link
  forces. If they have several strong links to nodes in the central area, they
  can be pulled inwards a bit, but otherwise they will end up outside the
  bubble distance. Similarly, nodes that have zero outgoing links are
  considered "passive" and are pushed out to an even further distance. Again
  strong connections may pull them inward slightly (and observing those cases
  can be interesting) but otherwise they will form an outer ring in the graph
  once fully relaxed.

  TODO: accuracy here

The bubble force in particular shapes the arrangement of the graph after enough
simulation of the physical forces has happened, which is why the "loose" and
"relaxed" layouts apply different amounts of simulation to relax the graph. The
"relax further" button can always be used to see the consequences of more
simulation updates, and dragging nodes also activates the simulation system.
The "loose" layout is an intermediate between the rigid grid of the "strict"
layout and the more circular appearance of the "relaxed" layout (which is due
to the bubble forces).


## Ego Network {#help:ego_network}

## Affinity Plot {#help:affinity_plot}

## Histograms {#help:histograms}

## Colors {#help:colors}

## Listing {#help:listing}
