Notes from GraphXD sprints
==========================

Also see the example folder for concrete code

From discussions with Nelle Varoquex, Aric, and Dan Shult
---------------------------------------------------------

- restrict to 'small' networks (few hundred to thousand)
- there are many choices in plotting mapping graph attributes -> visual properties

  - (x, y) layout
  - colors
  - labels
  - edges style
  - interactivity (hover / pick)
  - edge routing

- want to be able to update the plot in response to updating the network
- want to make it easily extensible
- performance?


From discussion with large group of network practitioners
---------------------------------------------------------

- need "seaborn for networks"
  - heursitics for edge style
- also want "seaborn for network statistics"
- look at igraph
  - have lots of layout engines
- people tend to use different plots for data exploration vs publication
- functions for different on graph size
- input to layout engine should be flexible
- provide way to go to the bottom!

ball and edge
~~~~~~~~~~~~~
- per-vertex/edges labels
- per-vertex/edges annotation box (maybe?)
- per-vertex/edge artists / subplots
  - excited about pie charts
  - do this as roll-over / tool-tip
- mark sub-graphs
- per-node style
- per-edge style
  - directed edges
  - un-directed edges
  - multi-edges
  - arbitrary path

adjacency matrix view
~~~~~~~~~~~~~~~~~~~~~
- show adjacency matrix
- show anything at all in the gutters (all 8 places)

trees
~~~~~

- dendograms

sankey / flow
~~~~~~~~~~~~~

- this may be better interface to the existing sankey functionality in
  Matplotlib

initial target cases
--------------------

- re-make jarod's slides
  - small (25 nodes)
- a 1000 node random graph
  - no labels, transparency, color per edge
- A tree of some sort
- splicing graph
- neural networks
- some flow network
