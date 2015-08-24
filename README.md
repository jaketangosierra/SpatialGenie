# SpatialGenie
This script is dependent on the following packages:

* numpy
* pysal
* tabulate
* argparse

All of these packages are available via pip.

This script is intended to take a shapefile ID (to differentiate rows), and path to the shapefile, and print out a tabulated Spatial Gini coefficient for each column in the shapefile DBF file.

> python SpatialGenie.py <id> <path>

There are other optional flags, including limiting the fields on which to calculate the Spatial Gini Coefficient

> python SpatialGenie.py <id> <path> --fields [field1 field2 field3]
