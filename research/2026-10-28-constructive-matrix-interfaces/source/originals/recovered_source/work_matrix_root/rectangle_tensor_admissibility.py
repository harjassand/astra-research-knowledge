#!/usr/bin/env python3
"""Exact tests of the direct N1077 interface for a folded three-factor sum.

These reject particular direct constructions.  They do not rule out a
different topology-changing representation or prove counting hardness.
"""
from pathlib import Path
from itertools import product
import json

def hyperdet(t):
    a,b,c,d,e,f,g,h=t
    return a*a*h*h+b*b*g*g+c*c*f*f+d*d*e*e-2*(a*b*g*h+a*c*f*h+a*d*e*h+b*c*f*g+b*d*e*g+c*d*e*f)+4*(a*d*f*g+b*c*e*h)

def determinant(a):return a[0][0]*a[1][1]-a[0][1]*a[1][0]

def transformed(t,matrices):
    result=[]
    for i,j,k in product(range(2),repeat=3):
        result.append(sum(matrices[0][i][x]*matrices[1][j][y]*matrices[2][k][z]
            *t[4*x+2*y+z] for x,y,z in product(range(2),repeat=3)))
    return result

def main():
    generic=[1,2,3,5,7,11,13,17]
    matrices=[[[1,2],[0,1]],[[2,1],[1,1]],[[1,0],[-3,2]]]
    multiplier=1
    for m in matrices:multiplier*=determinant(m)**2
    assert hyperdet(transformed(generic,matrices))==hyperdet(generic)*multiplier
    cases=[]
    for coefficients in ((1,1,1),(1,2,4),(3,-2,7)):
        a,b,c=coefficients;onehot=[0,c,b,0,a,0,0,0]
        assert hyperdet(onehot)==0
        moved=transformed(onehot,matrices)
        assert hyperdet(moved)==0
        cases.append(dict(one_particle_weights=coefficients,raw_tensor=onehot,
            hyperdeterminant=0,invertible_leg_transform=moved,transformed_hyperdeterminant=0))
    # Three factor hubs, three synchronized binary coordinates.  This is
    # exactly K_3,3; any connected gadget substitution retains it as a minor.
    factor_nodes=['bottom','top','folded_row'];copies=['mode0','mode1','mode2']
    edges=[(a,b) for a in factor_nodes for b in copies]
    vertices=len(factor_nodes)+len(copies)
    assert len(edges)>2*vertices-4 # Necessary edge bound for simple bipartite planar graphs.
    # An ordinary crossing has amplitudes 0000,1010,0101,1111 all +1.
    # With cyclic external order 1,2,3,4, a Gaussian tensor must obey
    # T0000*T1111=T1100*T0011-T1010*T0101+T1001*T0110.
    lhs=1;rhs=-1
    assert lhs-rhs==2
    out=dict(one_particle_source_cases=cases,
        three_layer_graph=dict(vertices=factor_nodes+copies,edges=edges,
            edge_count=len(edges),bipartite_planar_edge_bound=2*vertices-4,planar=False),
        ordinary_crossing=dict(Pfaffian_identity_left=lhs,Pfaffian_identity_right=rhs,defect=lhs-rhs,
            fermionic_crossing_changes_1111_to=-1),
        all_assertions_passed=True,
        scope='Direct N1077 input contract fails; no impossibility claim for a different representation')
    Path(__file__).with_name('rectangle_tensor_admissibility_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)

if __name__=='__main__':main()
