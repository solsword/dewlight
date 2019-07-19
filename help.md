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
graph).

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


## Controls {#help:controls}

 The global controls are:

- The "show" drop-down menu controls which view is displayed.
- The "filter nodes" check box controls whether all nodes are shown, or whether
  only important nodes are shown. It applies across all views, and also filters
  edges (only edges among included nodes are counted).
- the "node radius" slider which controls how large each node is in the graph
  views.
- The "clear selection" button allows you to deselect all currently selected
  nodes.
- The "mark" menu controls which nodes are marked with a symbol in the current
  view and the [listing](#help:listing). The symbols can help you see which
  node is which without hovering over it, but can also be distracting.


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

- The "hide" check boxes for "marginal edges" and "passive edges." These allow
  you to hide all edges that connect to marginal (or passive) nodes, to reduce
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

This view shows detailed information about all of the connections at a single
node. This focus node is in the center, and can be switched using a button in
the control panel based on the most-recently-selected node. All nodes that are
connected to the focus node are arrayed in a circle around the focus node,
ordered by their strength of connection with the focus node starting from 0
degrees on the right and proceeding clockwise. Strength of connection also
determines distance between the focus node and related nodes: the node that has
the strongest relationship is placed at 1/2 the base radius, and nodes with
weaker relationships are placed proportionally further out.

Unlike the other views, edges in this view are directional: each edge comes
from its source node, and ends before reaching the destination node. In cases
where an edge is not reciprocated, the edge ends 30% of the distance towards
the target, in other cases, the gap between the edges is placed between 15% and
85% of the distance between the nodes, according to the ratio between incoming
and outgoing weights. So a node that has a large weight on the edge from it to
the focus node but only a small weight on the reverse edge will have the edges
meet close to the focus node, and an node with opposite weights will have the
edges meet far from the focus node. The weights of edges are also explicit in
this view, instead of only being shown when an edge is hovered.

The controls for this view are:

- The "viewing" area displays the ID of the focus node, and the nearby "switch
  to" button allows you to switch the focus node to be the
  most-recently-selected node. If the most-recently selected node is the focus
  node itself, or if there aren't any selected nodes, the "switch to" button
  will be disabled.
- The "limit neighbors" drop-down menu offers options for limiting how many
  neighbors are displayed, which can be useful when a node has too many
  neighbors to easily see them all. The options include limiting to a certain #
  of nodes (ranked by weight of edges from and to the focus node), limiting to
  a certain # of interactions (the sum of edge weights in either direction),
  limiting to a certain % of interactions (relative to the node with the most
  interactions with the focus node), or limiting based on the presence of
  incoming, outgoing, and/or both types of links.

In this view, position around the circle, proximity to the central node, and
edge thicknesses all help answer the same question: Which other nodes are most
closely connected to the focus node? The lengths of paired directional edges to
and from each other node also show the balance of weights from and to the
central node. One-sided directional edges are also easy to spot, so you can
identify which nodes have one-way connections with the focus node.


## Affinity Plot {#help:affinity_plot}

The affinity plot shows the relative strength of relationship between one or
more inner nodes and a set of at least two outer nodes. The outer nodes are
arranged in a circle, and the inner nodes are placed within that circle
according to the strength of connection they have with each outer node.

In fact, the position of each inner node is just a weighted average of the
positions of the outer nodes, where the weights are the total weight of the
edges in both directions between the inner node and each outer node.

In some cases this causes overlap issues, but the plots are most informative
when you can see distinctions in how certain nodes are positioned within the
plot. Decreasing the node radius using the "node radius" slider may help in
cases where there is a lot of overlap.

The controls for this view are:

- The "hide exterior links" and "hide interior links" check boxes allow you to
  hide certain links. "Exterior" links are links between two outside nodes, and
  "interior" links are links between two inside nodes. Since the focus of the
  affinity plot is the links between the interior and exterior nodes, hiding
  links within those groups often makes sense.
- The "label edges" check box allows you to hide the numbers that show the
  strength of each edge (the placement of numbers also indicates which end of
  an edge had the higher initiated vs. received weight, although the exact
  breakdown is only shown in the [ego network](#help:ego_network) or by
  hovering over an edge. This can be useful when things get cluttered.
- The "update outside nodes" and "inside nodes" controls consist of four
  buttons that are normally disabled. When one or more nodes are selected, the
  first button in each group will be labeled with a '+' followed by a number
  indicating how many nodes will be added to that group (outside or inside)
  when the button is clicked, and the second button will have a '-', indicating
  how many nodes will be removed from the corresponding group. So for example,
  if you select a single node that's at the edge of the graph (an outside
  node), the second "update outside nodes" button will display "-1", and if you
  click it, that node will be removed from the outside nodes group. Because
  that node is already an outside node, the button to add outside notes will
  remain disabled, and the buttons for adding/removing inside nodes will also
  be unavailable (to make an outside node into an inside node, you must first
  remove it from the outside group and then add it to the inside group). To add
  nodes that aren't already part of the plot, select them using the
  [listing](#help:listing). The "clear selection" button may be useful in this
  view, because even after removing nodes from the plot, they remain selected.

In this view, the position of the outside node is fixed (they are sorted around
the circle by total edge weight, with ties broken by initiated edge weight and
then alphabetically by ID). The position of the inside nodes is determined by
which outside nodes they are most strongly connected to, however, and the
purpose of the affinity plot is to be able to compare these connection
strengths. If there are more than three outside nodes, position on the interior
is ambiguous: exactly which characters on one edge of the circle pulled the
node to that side should be inspected by looking at specific edges. So if two
inside nodes are close to each other, that doesn't necessarily mean that they
have exactly the same pattern of relationships with the exterior nodes.
However, if two nodes are placed differently, it *does* mean that they have
different relationship patterns, and if there are only two or three outside
nodes, then similar interior placement does imply similar relationships
patterns.

## Histograms {#help:histograms}

This view helps provide context for the edge weights used in the other views.
By displaying a histogram of values (such as interactions, which is total
initiated + received weight) this view gives a sense of how large or small a
particular value is relative to all of the nodes in the graph. Each histogram
displays a list of numbers along the x-axis, which are the distinct values
present among all nodes, and for each value, there's a bar indicating how many
nodes had that much total edge weight, with a number on top indicating the
precise count. So the x-axis is the combined edge weight (or # of neighbors)
depending on which graph is selected, and the y-axis is the total number of
nodes that have that combined edge weight (or # of neighbors).

This view can plot a histogram of the initiated weight, the received weight or
the initiated + received weight (interactions). It can also plot a histogram of
the number of neighbors each node has. In addition, you can select two
histograms at once and it will plot one above the x-axis and one below so you
can compare them visually (this really only makes sense for comparing among
initiated, received and initiated + received graphs).

The width of each bar is determined by how many bars can fit in the graph area,
but there is a minimum, and so if there are too many distinct values to
display, you will have to scroll the graph horizontally to see them all. The
height of the bars is determined such that the largest bar fills up the
available vertical space, so only relative heights are relevant. When two
graphs are shown, they are *not* scaled independently, so that the relative
height of bars above and below the x-axis can be compared directly.

The controls for this view are:

- The "graph" and "compare" selectors, along with a check box for "compare."
  The check box can be used to disable or enable comparison, and the selectors
  let you decide which values to plot.
- The "collapse values" check box controls how the x-axis is laid out. If
  checked (the default) then the x-axis will be compressed and numbers for
  which there is no node that has that much total weight (or that many
  neighbors) are not shown. This view makes it easier to see all of the bars at
  once, but means that distance along the x-axis is an unreliable indicator of
  relative total weight. If this box is unchecked, every integer will be shown
  on the x-axis up to the number for the node with the largest total weight (or
  largest neighborhood), which will usually force the graph to be scrolled to
  view all bars. Numbers where there are no corresponding nodes will have no
  bar above them. In this view, scrolling is usually necessary, but horizontal
  comparisons of position are valid.

In the histogram view, selection works a bit differently than in other views.
You can still use the [listing](#help:listing) to select individual nodes, and
this will highlight the bar(s) that they belong to (hovering on a bar will also
display the ID of all nodes associated with it, although in some cases the list
may be too long to fit on the screen). However, clicking on a bar will select
*all* nodes that belong to that bar, and any other bar(s) they belong to (in
the comparison view). Whether all or only some nodes at a bar are selected
(e.g., because they were selected using the listing), clicking on that bar
deselects all of them. So if you want to know which nodes have a total outgoing
weight of exactly 5, you can select the "initiated" histogram, and click on the
bar above the number 5 on the x-axis.

## Colors {#help:colors}

In the top-right of the window, there is a "Colors" panel which displays a
legend for the current graph. In the [relationships](#help:relationships), [ego
network](#help:ego_network), and [affinity plot](#help:affinity_plot) views,
this displays one color for each node group, along with the name of that group.
In the [histogram](#help:histogram) view, it displays the different colors used
for each different value that can be used to plot a histogram, which is useful
when comparing histograms to distinguish which is which.

TODO: group assignment tool in visualizer!
The groups and their names are defined as part of the dataset. If the dataset
was constructed using the included `build_graph.py` script, the groups will be
defined as follows:

- "Main" nodes have more than 1/2 as much total outgoing (initiated) weight as
  the single node with the largest outgoing weight.
- "Major" nodes have more than 1/3 as much total outgoing weight as the node
  with the largest outgoing weight.
- "Minor" nodes have more than 1/6 as much total outgoing weight as the node
  with the highest weight, *or* have more than the average (mean) outgoing
  weight.
- "Marginal" nodes do not qualify as "Minor" but have more than zero outgoing
  weight.
- "Passive" nodes have zero outgoing weight.

## Listing {#help:listing}

The listing area is on the right of the screen, and contains a list of all
nodes in the graph. It has controls for sorting or filtering nodes, and also
displays statistics for each node.

In every view except the ego network view, the stats displayed are total values
according to the whole graph: outgoing weight (labeled '🗣'), incoming weight
(labeled '👂'), combined weight (labeled '='), and number of distinct neighbors
(labeled '⇔'). The ego view displays the same stats, but except for the number
of neighbors, they are filtered to include only edges present in the currently
displayed ego network (in other words, only the weights on the edges to/from
the current focus node).

The controls for the listing area are:

- The "sort by" drop-down menu allows you to pick a property to sort by. Each
  property includes various fall-backs for breaking ties, usually in terms of
  whatever edge weights haven't been considered in the initial sort. The
  "default" sort order depends on the current view:
    * For the [relationships](#help:relationships) view, it sorts according to
      the order nodes were added to the layout (see details in that entry).
    * For the [ego network](#help:ego_network) view, it sorts according to the
      combined incoming and outgoing edge weight between each node and the
      current focus node, putting the focus node first. Nodes that don't appear
      in the current ego network are sorted to the bottom according to their
      group and then alphabetically by ID.
    * For the [affinity plot](#help:affinity_plot) view, it puts the outside
      characters first, then the inside characters, and then the rest of the
      characters, and in each group, it sorts by total weight of edges that
      connect just to the outside nodes (so for outside nodes, it sorts on
      connections among them, and for inside and other nodes, it sorts on their
      connection to the current outside node set). Ties on connections to the
      outside nodes are broken by total interactions, group, and then ID.
    * For the [histograms](#help:histograms) view the graph is sorted by the
      property used in the currently selected primary histogram (so outgoing
      weight, incoming weight, combined weight, or number of neighbors). These
      orderings, along with sorting by name and sorting by group and then game,
      are also available directly from the drop-down menu.
- The "find" text field allows you to type part of a node ID and the listing
  will be filtered as you type to show only nodes that contain the fragment
  you've typed as part of their ID (ignoring case). The clear button directly
  after the filter input just clears what you've typed and resets the filter;
  deleting everything in the text box also effectively resets the filter.
