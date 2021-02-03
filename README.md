# Dewlight

This project consist of open-source (see `LICENSE.txt`) code in
Javascript and Python for a network visualizer based on an interactions
list. The input is a tab-separated-value (TSV) file that lists
interactions with an "initiator" and one or more "recipients" for each
interaction. The Python code can transform this input into a JSON file
necessary to visualize the data, and it can also produce a bundled HTML
file that contains an interactive visualization for that data. The
Javascript code is included in that bundle and manages the visualization,
using the D3 visualization library as its primary engine.

This project was initially undertaken to visualize data on conversational
exchanges from the 17th century French novel "La Princesse de Clèves" by
Madame de La Fayette as a collaboration between Hélène Bilis and Peter
Mawhorter. That data was produced by Hélène Bilis and is included here
under a CC-BY 4.0 Creative Commons license (see `LICENSE-data.txt`). You
can find the raw data in the file `data/cleves.tsv`, and you can [see it
visualized here](https://solsword.github.io/dewlight/out/cleves-bundle.html).


## Operation & Dependencies

The `Makefile` contains recipes for building `.json` graph files from
`.tsv` input files and for building `-bundle.html` files from those
`.json` graph files. To fully operate the system, you will need the
following programs and modules.

- GNU Make to run the Makefile, or you can run the individual commands it
  contains in a terminal.

- Python 3 for:
    * building graphs (run `build_graph.py <TSV INPUT> -o <JSON OUPTUT>`)
    * bundling standalone HTML files (run `bundle.py <JSON INPUT>
      index.html` to produce `bundle.html`)
    * running a simple web server (run `python3 -m http.server` and then
      open [`https://localhost:8000`](https://localhost:8000) in your
      browser)

- If you don't have Python, running `chrome --allow-file-access-from-files`
  or a different browser with a similar ability to suspend CORS rules for
  files should allow you to open `index.html` and visualize the provided
  `example-graph.json` file (or a graph `.json` file of your choice,
  using `?t=...` at the end of your URL) without needing to run Python.

- If you want to include custom help text in your bundle, you can write
  that text in Markdown but you'll need to have Pandoc installed to
  convert it to HTML. You could also write your custom help text in HTML
  directly, or use the generic help text. You can run `bundle.py <JSON
  INPUT> index.html <HELP HTML FILE>` to include custom HTML help.


## Features:

- Build a network from a `.tsv` tab-separated-value file that lists initiated
  and received interactions.
- Automatically categorize nodes based on relative activity.
- Interactive node selection and labeling.
- Visualize a network in several ways:
    * Using a triangular grid layout where nodes are placed according to
      their interactions, with more-vocal characters near the center and
      with each character placed to minimize distance with their frequent
      interlocutors.
    * Using a force-directed graph based on the grid layout where
      low-interaction and non-initiating nodes are pushed to the edges.
    * As a histogram of initiated/received interaction counts.
    * As an ego network, showing direct connections from a selected node.
    * As an affinity plot, showing for several nodes their relative interaction
      levels with a group of framing nodes.
- Ability to sort & filter/find nodes in a list.
