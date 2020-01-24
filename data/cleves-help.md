# Help

## About {#help:about}

This page is a visualization tool for the novel “La Princesse de Clèves.” It
has multiple tools for visualizing connections between characters and
their relationships to each other. The visualization tools include:

- [Relationships](#help:relationships): This view shows the exchanges between
  all characters, with thicker lines connecting characters that interacted
  more frequently. It treats exchanges as reciprocal, and adds up the
  number of exchanges in both directions between every pair of characters.
  Characters are laid out on a grid so that those with more exchanges are
  closer to each other, and then a force simulation is used to relax their
  positions. This view gives a very high-level view of the overall connections
  between characters.
- [Ego Network](#help:ego_network): This view shows all of the exchanges from
  and to a single character. It displays initiated and received exchanges
  separately, and arranges interlocutors in a circle around the central
  character. This view gives a detailed view of all of the exchanges of a
  single character, at the cost of hiding interactions between other
  characters.
- [Affinity Plot](#help:affinity_plot): This view shows, for an “inner” group
  of characters,  the relative number of exchanges with an “outer” group of
  reference characters. The reference characters are placed on the perimeter of
  a circle, and characters of interest are placed inside, located based on
  their relative number of exchanges with each outer character. Like the
  relationships graph the affinity plot treats exchanges as reciprocal. This
  view is designed to highlight differences in character relationships between
  a few characters at a time; it becomes ambiguous with more than 4 or 5
  reference characters.
- [Histograms](#help:histograms): This view provides a more abstract view of
  the characters, showing a histogram of one of several properties, like the
  number of exchanges each character initiated, or the number of distinct
  characters each character interacted with (“neighbors”). It can also display
  two histograms simultaneously to compare them. This view is the most
  abstract, but can be used to get an overall sense for the exchange numbers
  displayed in the other views.

At the top left, the controls area shows [global controls](#help:controls) and
graph-specific controls (described in the help sections for each type of
graph).

At the top right, there is a legend that shows the styles used for the current
view. For most views, style is based on group, which is discussed in the
[legend](#help:legend) section.

On the bottom left, the current view is displayed. In all views, you can click
on characters (or bars in the [histograms](#help:histograms) view) to select
them. Selections filter which edges are visible, and also control how the [ego
network](#help:ego_network) and [affinity plot](#help:affinity_plot) views
behave.

On the bottom right, the [listing](#help:listing) displays the name of each
character, along with its assigned label (if any), the number of initiated, received, and total exchanges for that character, and the number of different characters it interacted with (“neighbors”).


## Controls {#help:controls}

The global controls are:

- The “show” drop-down menu controls which view is displayed.
- The “core groups only” check box controls whether all characters are shown, or
  whether only important characters are shown. It applies across all views, and
  also filters edges (only edges among included characters are counted).
- the “marker size” slider which controls how large each symbol is in the graph
  views.
- The “clear selection” button allows you to deselect all currently selected
  characters.
- The “mark” menu controls which characters are marked with a label in the
  current view and the [listing](#help:listing). The label can help you see
  which character is which without hovering over it, but can also be
  distracting.
- The “transparency” check box controls whether character symbols are displayed
  using solid or transparent colors. Transparency helps the labels stand out a
  bit more, especially if you are going to display a visualization in
  grayscale.


## Relationships {#help:relationships}

The relationships view displays the connections among characters, using an
automatic layout that tries to put more-frequent interlocutors closer to each
other, starting from the character with the most total exchanges. The positions
in the graph can thus be interpreted (with caution) as implying relationships
among characters. These should be confirmed with reference to the text itself,
as number-of-interactions is only a vague proxy for strength-of-relationship,
but cases where the two differ drastically may be interesting in their own
right.

You can drag around the characters to adjust their position, but when you do
that, the rest of the characters will be allowed to move according to their
constraints, and those constraints may counteract your intended motion.
By hovering over a character or selecting one or more characters (by clicking
on them), you can limit which edges are shown, and hovering on a character or
edge for a few seconds will display detailed information about it.

The controls for this view are:

- The “hide” check boxes for “marginal edges” and “passive edges.” These allow
  you to hide all edges that connect to marginal (or passive) characters, to
  reduce clutter.
- The “layout” selector, which allows you to switch between the “strict,”
  “loose,” and “relaxed” layouts (see below).
- The “reset layout” button, which puts characters back to their original
  positions for the selected layout.
- The “relax further” button, which allows the characters to settle more under
  the physical simulation rules (see below).

The position of the characters is governed by two processes: the initial
layout, and a physical simulation that includes several simulated forces.

### Initial Layout

The initial layout results can be viewed without running the physical
simulation at all by selecting the “strict” layout option. This layout places
characters on a triangular grid. To produce this layout, the following
algorithm is used:

1. At each step, select a character to place:
    - For the first step, use the character that has the highest total number
      of exchanges (initiated plus received).
    - For subsequent steps, pick the character that has the most exchanges
      (initiated plus recevied) with characters that have already been placed.
      Ties are broken by total exchanges with any character (including those
      not placed so far), then by number of neighbors, then by group
      (more-interacting groups first; see [legend](#help:legend)), and finally
      by alphabetical order of character names.
2. Next, place that character:
    - For the first step, place it at the origin (0, 0).
    - For subsequent characters, examine all empty grid locations that are
      adjacent to an already-placed character:
          * At each location, compute the cost for that location as the
            weighted sum of the edge lengths from this character to each
            character that's already been placed. This is just the length
            of each edge (if the character were at this location) times the
            number of exchanges between the two characters the edge connects.
          * Pick the location that has the lowest total cost, and put the
            character there. Ties are broken by choosing locations that are
            closer to the origin, and double-ties are broken by choosing the
            edge position that was added to the list of edge positions first.
3. Finally, repeat steps 1 and 2 until all characters have been placed
   (including characters not connected to the original character).

This algorithm normally results in a roughly hexagonal grouping of characters,
even when connections aren't thick, because it breaks ties towards the origin.
The default listing sort order for this view shows the order in which
characters were added, which can help understand the layout, but in general,
and especially for the first several characters placed, proximity in the layout
indicates relative strength of connection (as things get crowded the grid
constraints make this less strictly true).

Once the characters are positioned in this grid, in the “loose” and “relaxed”
layouts, those positions are relaxed by simulating a few physical forces acting
on the characters in two dimensions.

### Physical Simulation

When the “relax” further button is clicked, when a character is dragged, or
during layout construction for the “loose” and “relaxed” layouts, physical
forces are simulated to position the characters. The two main forces are:

- A repulsion force that pushes all characters away from each other when they
  get too close. This prevents characters from piling up and obscuring each
  other, but it also is the primary source of distortion that causes characters
  *not* to be positioned as close to their neighbors as they would naturally
  be.
- An attraction force along each edge, which, as long as the characters aren't
  overlapping, pulls them closer to each other, and gets stronger the farther
  the edge is stretched. The strength of the attraction force is also
  proportional to the logarithm of the exchanges between the characters, so
  edges between characters that interact frequently pull a bit harder (but it's
  not a huge difference).

In addition to these two main forces, there are several more forces to help
arrange the characters:

- A gathering force pulls all characters towards the origin. This ensures that
  disconnected characters do not drift away from the main part of the graph.
  This force is fairly weak, so it does not introduce very much distortion.
- A “bubble” force that forces characters in certain categories out of the
  center of the graph. Characters in the “marginal” group (see
  [legend](#help:legend)) are all pushed outward from the center a set distance
  by a very strong force that's stronger than most other forces. If they have
  several strong connections to characters in the central area, they can be
  pulled inwards a bit, but otherwise they will end up outside the bubble
  distance. Similarly, characters in the “passive” group are pushed out to an
  even further distance. Again strong connections may pull them inward slightly
  (and observing those cases can be interesting) but otherwise they will form
  an outer ring in the graph once fully relaxed.

The bubble force in particular shapes the arrangement of the graph after enough
simulation of the physical forces has happened, which is why the “loose” and
“relaxed” layouts apply different amounts of simulation to relax the graph. The
“relax further” button can always be used to see the consequences of more
simulation updates, and dragging characters also activates the simulation
system. The “loose” layout is an intermediate between the rigid grid of the
“strict” layout and the more circular appearance of the “relaxed” layout (which
is due to the bubble forces).


## Ego Network {#help:ego_network}

This view shows detailed information about all of the exchanges initiated by
and received by a single character. This focus character is in the center, and
can be switched using the “switch to” button in the control panel based on the
most-recently-selected character. All characters that interact with the focus
character are arrayed in a circle around the focus character, ordered by
their number of exchanges with the focus character starting from 0 degrees
on the right and proceeding clockwise. Number of exchanges also determines
distance between the focus character and their interlocutors: the character
that interacted the most is placed at 1/2 the full radius, and characters with
weaker relationships are placed proportionally further out.

Unlike the other views, edges in this view are directional: each edge comes
from its initiating character, and ends before reaching the receiving
character. In cases where exchanges are not reciprocal, the edge from the
character who initiated all exchanges ends 30% of the distance towards the
target, in other cases, the gap between the edges is placed between
15% and 85% of the distance between the characters, according to the ratio
between initiated and received exchanges. So a character that initiated many
exchanges with the focus character but only received a few in return will have
the edges meet close to the focus character, and a character who received many
exchanges from the focus character but initiated few with them will have the
edges meet far from the focus character. The number of exchanges are also
explicit in this view (they are displayed at the end of each edge), instead of
only being shown when an edge is hovered.

The controls for this view are:

- The “viewing” area displays the name of the focus character, and the nearby
  “switch to” button allows you to switch to focus on the
  most-recently-selected character. If the most-recently selected character is
  already the focus character, or if no characters are selected, the “switch
  to” button will be disabled.
- The “limit neighbors” drop-down menu offers options for limiting how many
  interlocutors are displayed, which can be useful when a character has
  interacted with too many other characters to easily see them all. The options
  include limiting to a certain # of characters (ranked by number of exchanges
  with the focus character), limiting to a certain # of interactions with the
  focus character, limiting to a certain % of interactions (relative to the
  character with the most interactions with the focus character), or limiting
  based on the presence of incoming, outgoing, and/or both types of edge.

In this view, position around the circle, proximity to the central character,
and edge thicknesses all help answer the same question: Which other characters
are most closely connected to the focus character? The lengths of paired
directional edges to and from each other character also show the balance of
exchanges initiated between that character and the focus character. One-sided
directional edges are easy to spot, so you can identify which characters have
one-sided exchanges with the focus character.

In the [listing](#help:listing) for this view, the exchange numbers shown
(initiated, received, and total) include only exchanges with the current focus
character (so they match the numbers shown on the edges of the graph), and the
default ordering is according to total interactions with the focus character
(which matches the ordering of each character around the circle). The number of
neighbors in the listing is still the full number of other characters
interacted with.

## Affinity Plot {#help:affinity_plot}

The affinity plot shows the relative number of exchanges between one or more
“inner” characters and a set of at least two “outer” characters. The outer
characters are arranged in a circle, and the inner characters are placed within
that circle according to the number of exchanges between them and each outer
character.

In fact, the position of each inner character is just a weighted average of the
positions of the outer characters, where the weights are the total number of
exchanges between the inner character and each outer character.

In some cases this causes overlap issues, but the plots are most informative
when you can see distinctions in how certain characters are positioned.
Decreasing the symbol size using the “marker size” slider may help in cases
where there is a lot of overlap, and characters can always be selected using
the listing, which filters which edges are displayed.

The controls for this view are:

- The “hide exterior links” and “hide interior links” check boxes allow you to
  hide certain edges. “Exterior links” are edges between two outer characters,
  and “interior links” are edges between two inner characters. Since the focus
  of the affinity plot is the links between the inner and outer characters,
  hiding links within those groups usually makes sense, and the exterior links
  are hidden by default.
- The “label edges” check box allows you to hide the numbers that show the
  interactions for each edge (the placement of numbers also indicates which end
  of an edge had the higher initiated vs. received weight, although the exact
  breakdown is only shown in the [ego network](#help:ego_network) or by
  hovering over an edge. This can be useful when things get cluttered.
- The “update outer” and “update inner” controls consist of four buttons that
  are normally disabled. When one or more characters are selected, the
  first button in each group will be labeled with a “+” followed by a number
  indicating how many characters would be added to that group (outer or
  inner) if the button is clicked, and the second button will have a “-,”
  indicating how many characters would be removed from the corresponding group.
  So for example, if you select a single character that's at the edge of the
  graph (an outer character), the second “update outer” button will display
  “-1”, and if you click it, that character will be removed from the outer
  characters group. Because that character is already an outer character, the
  button to add outside characters will remain disabled, and the buttons for
  adding/removing inside characters will also be unavailable (to make an
  outer character into an inner character, you must first remove it from the
  outer group and then add it to the inner group). To add characters that
  aren't already part of the plot, select them using the
  [listing](#help:listing). The “clear selection” button may be useful in this
  view, because even after removing characters from the plot, they remain
  selected.

In this view, the positions of the outer characters are fixed (they are sorted
around the circle by total number of interactions, with ties broken by
initiated interactions and then alphabetically by name). The position of the
inner characters is determined by which outer characters they interact with the
most, however, and the purpose of the affinity plot is to be able to compare
these interaction numbers. If there are more than four outer characters,
position on the interior is ambiguous: exactly which character(s) on one edge
of the circle pulled an inner character to a side should be inspected by
looking at specific edges (selecting the inner character helps).

So if two inner characters are positioned close to each other, that doesn't
necessarily mean that they have similar patterns of interaction with the outer
characters. However, if two characters are placed differently, it *does* mean
that they have different interaction patterns, and if there are four or fewer
outer characters, then similar interior placement does imply similar
interaction patterns (in terms of total interactions between characters).

Note that proximity of inner characters (and of outer characters) has nothing
to do with relationships *among* inner (or outer) characters. Only the
interactions involving both an inner and an outer character are used to
determine positions in this view.

## Histograms {#help:histograms}

This view helps provide context for the interaction numbers used in the other
views. By displaying a histogram of values this view gives a sense of how large
or small a particular value is relative to the values for all characters. Each
histogram displays a list of numbers along the x-axis, which are the distinct
values present among all characters, and for each value, there's a bar
indicating how many characters had that value, with a number on top indicating
the precise count. So the x-axis is the combined exchange count (or # of
neighbors, depending on which graph is selected), and the y-axis is the total
number of characters that have that combined count (or # of neighbors).

This view can plot a histogram of just initiated exchanges, just received
exchanges or total interactions (initiated plus received). It can also plot a
histogram of the number of neighbors each character has (i.e., number of other
characters they interacted with at least once). In addition, you can select two
histograms at once and it will plot one above the x-axis and one below so you
can compare them visually (this really only makes sense for comparing among
initiated, received, and initiated + received graphs).

The width of each bar is determined by how many bars can fit in the graph area,
but there is a minimum, and so if there are too many distinct values to
display, you will have to scroll the graph horizontally to see them all. The
height of the bars is determined such that the largest bar fills up the
available vertical space, so only relative heights are relevant. When two
graphs are shown, their scales are matched, so that the relative height of bars
above and below the x-axis can be compared directly.

The controls for this view are:

- The “graph” and “compare” selectors, along with a check box for “compare”.
  The check box can be used to disable or enable comparison, and the selectors
  let you decide which values to plot.
- The “collapse values” check box controls how the x-axis is laid out. If
  checked (the default) then the x-axis will be compressed and numbers for
  which there is no character that has that many exchanges (or that many
  neighbors) are not shown. This view makes it easier to see all of the bars at
  once, but means that distance along the x-axis is an unreliable indicator of
  relative values. If this box is unchecked, every integer will be shown
  on the x-axis up to the number for the character with the largest total
  value, which may force the graph to be scrolled quite far to view all bars.
  Numbers where there are no corresponding characters will have no bar above
  them. In this view, scrolling is almost always necessary, but horizontal
  comparisons of position make sense.

In the histogram view, selection works a bit differently than in other views.
You can still use the [listing](#help:listing) to select individual characters,
and this will highlight the bar(s) that they belong to (hovering on a bar will
also display the ID of all characters associated with it, although in some
cases the list may be too long to fit on the screen). However, clicking on a
bar will select *all* characters that belong to that bar, and any other bar(s)
they belong to (in the comparison view). Whether all or only some characters at
a bar are selected (e.g., because they were selected using the listing),
clicking on that bar deselects all of them. So for example, if you want to know
which characters initiated exactly 5 exchanges, you can select the
“initiated” histogram, and then either hover over the bar above the number 5 on
the x-axis, or click on it and look at which characters are bolded in the
listing.

## Legend {#help:legend}

In the top-right of the window, there is a “Legend” panel which displays a
legend for the current graph. In the [relationships](#help:relationships), [ego
network](#help:ego_network), and [affinity plot](#help:affinity_plot) views,
this displays one style for each character group, along with the name of that
group. In the [histogram](#help:histogram) view, it displays the different
styles used for each different value that can be used to plot a histogram,
which is useful when comparing histograms to distinguish which is which.

The character groupings are as follows:

- “Main” characters are the princess, the prince, and Nemours. Each of them
  initiated at least 1/2 as many total exchanges as the princess, who is the
  focal character of the novel, and no other characters reached that threshold.
- “Major” characters are the King (Henry II), and the Dauphine, who each
  initiated at least 1/3 as many exchanges as the princess.
- “Minor” characters are Vidame, Catherine de Médicis, Mme. de Chartres, Mme.
  de Martigues, and Sancerre, who each initiated more exchanges than the
  average across all characters (which was 8.3).
- “Special” characters are the “impersonal character,” (either constructions in
  the passive voice, or the French impersonal pronoun “on”), and “La cour,” or
  “the court,” which records instances where the court as a group speaks or is
  spoken to. They each have unique patterns of interaction and are interesting
  in their own right.
- “Marginal” characters are all other characters who do not qualify as “Minor”
  but who participated in at least two exchanges.
- “Scarce” characters are characters who participated in just a single exchange.

## Listing {#help:listing}

The listing area is on the right of the screen, and contains a list of all
characters in the graph. It has controls for sorting or filtering characters,
and also displays statistics for each character.

In every view except the ego network view, the stats displayed are total values
according to the whole graph: exchanges initiated (labeled '🗣'), exchanges
received (labeled '👂'), total interactions (labeled '='), and number of
distinct neighbors (labeled '⇔'). The ego view displays the same stats, but
except for the number of neighbors, they are filtered to include only edges
present in the currently displayed ego network (in other words, only
interactions involving the current focus character).

The controls for the listing area are:

- The “sort by” drop-down menu allows you to pick a property to sort by. Each
  property includes various fall-backs for breaking ties, usually in terms of
  whatever stats haven't been considered in the initial sort. The “default”
  sort order depends on the current view:
    * For the [relationships](#help:relationships) view, it sorts according to
      the order characters were added to the layout (see details in that entry).
    * For the [ego network](#help:ego_network) view, it sorts according to the
      combined incoming and outgoing edge weight between each character and the
      current focus character, putting the focus character first. Characters
      that don't appear in the current ego network are sorted to the bottom
      according to their group and then alphabetically by name.
    * For the [affinity plot](#help:affinity_plot) view, it puts the outer
      characters first, then the inner characters, and then the rest of the
      characters, and in each group, it sorts by exchanges with just the
      outer characters (so for outer characters, it sorts on
      interactions among them, and for inner and other characters, it sorts on
      their interactions with the current outside character set). Ties on
      connections to the outside characters are broken by total interactions,
      group, and then name.
    * For the [histograms](#help:histograms) view the graph is sorted by the
      property used in the currently selected primary histogram (so initiated
      exchanges, received exchanges, total interactions, or number of
      neighbors). These orderings, along with sorting by name and sorting by
      group and then name, are also available directly from the drop-down menu.
- The “find” text field allows you to type part of a character name and the
  listing will be filtered as you type to show only characters whose names
  contain the fragment you've typed (ignoring case). The clear button directly
  after the filter input just clears what you've typed and resets the filter;
  deleting everything in the text box also effectively resets the filter.
