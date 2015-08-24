import pysal
import numpy
import argparse
from tabulate import tabulate

parser = argparse.ArgumentParser(description='Finds the spatial Gini coefficient from a shapefile')
parser.add_argument('id', help='the id field in the shapefile')
parser.add_argument('shapefile', metavar='shp', help='a shapefile path')
parser.add_argument('-l', '--latex', help='produces latex output', action="store_true")
parser.add_argument('-m', '--pandoc', help='produces pandoc-flavored markdown output', action="store_true")
parser.add_argument('-ht', '--html', help='produces html output', action="store_true")
parser.add_argument('-w', '--mediawiki', help='produces mediawiki output', action="store_true")
parser.add_argument('--fields', nargs='+', help='fields to run Gini on, if left off, runs on all numeric fields')
args = parser.parse_args();

table_format = 'simple'
if args.latex:
	table_format = 'latex'

if args.html:
	table_format = 'html'

if args.mediawiki:
	tbale_format = 'mediawiki'

if args.pandoc:
	tbale_format = 'simple'

weights = pysal.weights.user.queen_from_shapefile(args.shapefile, args.id.upper())
weights.transform='B'
dbf = pysal.open(args.shapefile.replace("shp", "dbf"))
out = [['COLUMN', 'GINI', 'NEIGHBOR INEQUALITY', 'NON-NEIGHBOR INEQUALITY', 'SHARE OF INEQUALITY IN NON-NEIGHBOR', 'P-VALUE', 'THEIL']]

if not args.fields:
	args.fields = dbf.header
	tmp = dbf.field_spec
	for i, field in enumerate(tmp):
		if field[0] == 'C':
			args.fields.pop(i)

for f in args.fields:
	name = f.upper()
	col = dbf.by_col(name)
	arr = numpy.array(col)
	gini = pysal.inequality.gini.Gini_Spatial(arr, weights)
	theil = pysal.inequality.theil.Theil(arr)

	out.append([name, gini.g, gini.wg, gini.wcg, gini.wcg_share, gini.p_sim, theil.T])

print tabulate(out, headers="firstrow", tablefmt=table_format, numalign="right", floatfmt='.4f')
