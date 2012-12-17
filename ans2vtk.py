#!/usr/bin/env python

import numpy as np


def writefile(filename,nodes, nodedict, elements, elemdict,nodedata={}, vecnodedata={}):
    nonr=len(nodes)
    elnr=len(elements)
    print 'Nbr. Nodes: ',nonr
    print 'Nbr. Elements: ', elnr
    f=open(filename,'w')
    f.writelines('# vtk DataFile Version 2.0\nAnsys 2 VTK\nASCII\nDATASET UNSTRUCTURED_GRID\n')
    f.write('POINTS %d float\n'%nonr)
    for i in range(nonr):
        #f.write('%f %f %f\n'%tuple(nodes[i]))
        f.write('%s %s %s\n'%tuple(nodes[i]))
    f.write('CELLS %d %d\n'%(elnr,elnr*9))
    for n in range(elnr):
    #    f.write('8 %d %d %d %d %d %d %d %d\n'%tuple([nodedict[x]-1 for x in elements[n]]))
        f.write('8 %d %d %d %d %d %d %d %d\n'%tuple([nodedict[i] for i in elements[n]]))
    f.write('\nCELL_TYPES %d\n'%elnr)
    for j in range(elnr):
        f.write('23\n')
    if len(nodedata) == 0: return 0
    f.write('\nPOINT_DATA %d\n'%nonr)
    for dat in nodedata:
        f.write('\nSCALARS {0} float 1\nLOOKUP_Table default\n'.format(dat))
        for k in range(nonr):
            f.write('%g \n'%nodedata[dat][k])
    #for idx,case in enumerate(nodedata):
    for dat in vecnodedata:
        f.write('VECTORS {0} float\n'.format(dat))
        for j in range(nonr):
            f.write('{0[0]} {0[1]} {0[2]} \n'.format(vecnodedata[dat][j]))
    #f.write('\nSCALARS SPCForces_X float 1\nLOOKUP_Table default\n')
    #for k in range(0,len(nodedisp),2):
    #    f.write('%g\n'%(spcvec[k]))
    #f.write('\nSCALARS SPCForces_Y float 1\nLOOKUP_Table default\n')
    #for k in range(0,len(nodedisp),2):
    #    f.write('%g\n'%(spcvec[k+1]))
    f.close()

def read_nodes(filen, nodes, nodedict):
    fil = open(filen,'r')
    ncount = 0
    while fil:
        fline = fil.readline().split()
        if len(fline) < 4: return 0
        nodedict[fline[0]] = ncount
        nodes.append(fline[1:4])
        ncount += 1
    fil.close()

def read_elements(filen, elements, elemdict):
    fil = open(filen,'r')
    ecount = 0
    while fil:
        fline = fil.readline().split()
        if len(fline) < 8: return 0
        elemdict[int(fline[-1])] = ecount
        elements.append(fline[0:8])
        ecount += 1
    fil.close()


if __name__=="__main__":
    
    nodefile = 'submodsm6_v01.node'
    elfile   = 'submodsm6_v01.elem'

    nodes = []
    elements = []
    nodedict = {}
    elemdict = {}
    nodedata = {}
    vecnodedata = {}

    read_nodes(nodefile,nodes,nodedict)
    read_elements(elfile,elements,elemdict)

    # some arbitrary data
    from numpy.random import random
    nodedata['Random'] = random(len(nodes))
    nodedata['Sin'] = np.sin(np.linspace(0,2*np.pi,len(nodes)))
    backlist = dict((v,k) for k,v in nodedict.iteritems())
    nodedata['Nbr'] = [int(backlist[i]) for i in range(len(nodes))]

    # vecdata
    vecnodedata['VecF1'] = zip(random(len(nodes)),np.zeros(len(nodes)), random(len(nodes)))
    
    writefile('geo.vtk',nodes, nodedict, elements, elemdict, nodedata, vecnodedata)
    print 'finished'
