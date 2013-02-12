# GraphML-Topo-to-Mininet-Network-Generator
#
# This file parses Network Topologies in GraphML format from the Internet Topology Zoo.
# A python file for creating Mininet Topologies will be created as Output.
# Files have to be in the same directory.
#
# Arguments:
#   TODO : make extensions optional
#   -f          [filename to of GraphML input file]
#   --file      [filename to of GraphML input file]
#   -o          [filename to of GraphML output file]
#   --output    [filename to of GraphML output file]
#
# Without specified input, program will terminate.
# Without specified output, outputfile will have the same name as the input file.
#
#
# Created by Stephan Schuberth in 01/2013

# === stuff to be added ===
#dist(SP,EP) = arccos{ sin(La[EP]) * sin(La[SP]) +  cos(La[EP]) * cos(La[SP]) * cos(Lo[EP] - Lo[SP])} * r
#r = 6378.137 km


import xml.etree.ElementTree as ET
import sys
from sys import argv

inputfilename = ''
outputfilename = ''

# TODO use 'argparse', the built-in argument parser of python
# first check commandline arguments
for i in range(len(argv)):
    if argv[i] == '-f':
        inputfilename = argv[i+1]
    if argv[i] == '--file':
        inputfilename = argv[i+1]
    if argv[i] == '-o':
        outputfilename = argv[i+1]
    if argv[i] == '--output':
        outputfilename = argv[i+1]

# terminate when inputfile is missing
if inputfilename == '':
    sys.exit('\n\tno input file was specified as argument')

# define string fragments for output later on
# TODO fix several outputstrings to be one preformatted string
outputstring_1 = '''"""
Custom topology for Mininet, generated by GraphML-Topo-to-Mininet-Network-Generator.
"""

from mininet.topo import Topo, Node

class GeneratedTopo( Topo ):
    "Internet Topology Zoo Specimen."

    def __init__( self, enable_all = True ):
        "Create topology."

        # Add default members to class.
        super( GeneratedTopo, self ).__init__()

        # Set Node IDs for hosts and switches
'''

outputstring_2='''
        # Add nodes
        #switches
'''

outputstring_3='''
        # edd edges
'''

outputstring_4='''
        # Consider all switches and hosts 'on'
        self.enable_all()

topos = { 'generated': ( lambda: GeneratedTopo() ) }
'''

# where to put results
outputstring_to_be_exported = ''
outputstring_to_be_exported += outputstring_1

# read file and do the actual parsing
tree = ET.parse(inputfilename)
namespace = "{http://graphml.graphdrawing.org/xmlns}"
ns = namespace # just doing shortcutting, namespaces are needed often.

root = tree.getroot()
graph = root.find(ns + 'graph')

#get all entries
nodes = graph.findall(ns + 'node')
edges = graph.findall(ns + 'edge')

# now first generate the id's
node_root_attrib = ''
node_name = ''
id_node_dict = {} # to hold all 'id: name' pairs

#get id data
for n in nodes:
    node_root_attrib = n.attrib['id']
    data = n.findall(ns + 'data')
    for d in data:
        if d.attrib['key'] == 'd34':
            node_name = d.text
        #save data couple
        id_node_dict[node_root_attrib] = node_name
#create strings
tempstring = ''
for i in range(0, len(id_node_dict)):
    temp = id_node_dict[str(i)]
    tempstring += '        '
    tempstring += temp
    tempstring += ' = '
    tempstring += str(i)
    tempstring += '\n'
outputstring_to_be_exported += tempstring
outputstring_to_be_exported += outputstring_2

# second create the nodes sections
tempstring = ''
for i in range(0, len(id_node_dict)):
    temp =  '        self.add_node( '
    temp += id_node_dict[str(i)]
    temp += ', Node( is_switch=True ) )\n'
    tempstring += temp
outputstring_to_be_exported += tempstring
outputstring_to_be_exported += outputstring_3

# third create the edges
tempstring = ''
for e in edges:
    temp =  '        self.add_edge( '
    temp += id_node_dict[e.attrib['source']]
    temp += ' , '
    temp += id_node_dict[e.attrib['target']]
    temp += ' )\n'
    tempstring += temp

outputstring_to_be_exported += tempstring
outputstring_to_be_exported += outputstring_4

# generation finished, write string to file
outputfile = ''
if outputfilename == '':
    outputfilename = inputfilename + '-generated-Mininet-Topo.py'
outputfile = open(outputfilename, 'w')
outputfile.write(outputstring_to_be_exported)
outputfile.close()
